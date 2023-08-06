# common_functions.py

import pandas as pd
import numpy as np
import pymssql
import mssql_auth
import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator
from tslearn.clustering import KShape
from datetime import datetime
import time
import math
import threading
import gc
import warnings
warnings.filterwarnings(action="ignore")

login = mssql_auth.info


class Common:

    __host = login["host"]
    __user = login["user"]
    __password = login["passwd"]
    __database = login["database"]
    __charset = login["charset"]
    sitecode = ""

    def __init__(self, sitecode):
        self.sitecode = sitecode
        Common.sitecode = sitecode

    # MSSQL 접속
    @classmethod
    def conn(cls):
        return pymssql.connect(cls.__host, cls.__user, cls.__password, cls.__database, charset='UTF8')

    # 운영지점 코드 (T_SITE_INFORMATION)
    # noinspection PyMethodMayBeStatic
    def site_code(self):
        db = Common.conn()
        cursor = db.cursor()
        cursor.execute("SELECT top 1 ltrim(SiteCode) FROM T_SITE_INFORMATION WHERE OperationYN = 'Y' ")

        all_row = cursor.fetchall()
        scode = all_row[0][0]
        cursor.close()
        db.close()

        Common.sitecode = scode
        return scode

    # 부하보정일수, 보정기준시각 (운영환경 테이블)
    # noinspection PyMethodMayBeStatic
    def wokr_time(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT left(WorkStartTime,2), left(WorkStopTime, 2) \
                 FROM T_OPERATING_CONFIG \
                WHERE sitecode = '" + Common.sitecode + "' "
        cursor.execute(sql)

        # 실행문 조회
        worktime = cursor.fetchall()
        if worktime == []:
            workstarttime = 0
            workstarttime = 0
        workstarttime = worktime[0][0]
        workstoptime = worktime[0][1]

        cursor.close()
        db.close()
        return workstarttime, workstoptime

    # noinspection PyMethodMayBeStatic
    def select_power_real_15m(self, e_src):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  CONVERT(VARCHAR(19), (RealDate+LEFT(RealHour,2)+RealMin), 20) AS Savetime, \
                       RealDate, LEFT(RealHour,2) AS RealHour, RealMin, RealPower15M, WeekHoliday \
                 FROM T_POWER_REAL_15M \
                WHERE SiteCode = '" + Common.sitecode + "' \
                  AND EnergySource = '" + str(e_src) + "' \
                ORDER BY Savetime "

        df_power_predict15m = pd.read_sql(sql, db)
        cursor.close()
        db.close()

        return df_power_predict15m

    # noinspection PyMethodMayBeStatic
    def count_power_real_15m(self, e_src, before_time, current_time):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT  COUNT(*), SUM(RealPower15M) AS RealPower15M \
                 FROM T_POWER_REAL_15M \
                WHERE SiteCode = '" + Common.sitecode + "' \
                  AND EnergySource = '" + str(e_src) + "' \
                  AND CONVERT(VARCHAR(19), (RealDate+LEFT(RealHour,2)+RealMin), 20) \
                                  BETWEEN '" + before_time + "' AND '" +current_time + "' "

        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        count_15m = all_fetch[0][0]
        sum_realpower15m = all_fetch[0][1]

        cursor.close()
        db.close()

        return count_15m, sum_realpower15m

    # noinspection PyMethodMayBeStatic
    def weather_real_info(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT ANNOUNCEDATE as Date, LEFT(ANNOUNCEHOUR,2) as Hour, REALREH as Reh, REALTEMP as Temp \
                 FROM T_1HOUR_WEATHER_REAL_INFO \
                WHERE SiteCode = '" + Common.sitecode + "' \
                ORDER BY ANNOUNCEDATE "

        weather_real = pd.read_sql(sql, db)

        cursor.close()
        db.close()

        return weather_real

    # noinspection PyMethodMayBeStatic
    def weather_predict_info(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT PREDICTIONDATE as Date, LEFT(PREDICTIONHOUR,2) as Hour, PREDICTIONREH as Reh, PREDICTIONTEMP as Temp \
                 FROM T_1HOUR_WEATHER_PREDICT_INFO \
                WHERE SiteCode = '" + Common.sitecode + "' \
                ORDER BY PREDICTIONDATE "

        weather_predict = pd.read_sql(sql, db)

        cursor.close()
        db.close()

        return weather_predict

    # noinspection PyMethodMayBeStatic
    def get_holiday_day(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT HOLIDAYCODE FROM T_SITE_INFORMATION \
                WHERE SiteCode = '" + Common.sitecode + "' "
        cursor.execute(sql)
        holiday = cursor.fetchall()
        holiday_idx = holiday[0][0]

        cursor.close()
        db.close()
        return holiday_idx

    # noinspection PyMethodMayBeStatic
    def get_holiday(self, startdate, enddate):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT holiday FROM T_HOLIDAY \
                WHERE sitecode = '" + Common.sitecode + "' \
                  AND holiday BETWEEN '" + startdate + "' AND '" + enddate + "' "
        df_holiday = pd.read_sql(sql, db)

        cursor.close()
        db.close()
        return df_holiday

    # 공휴일인지 체크
    # noinspection PyMethodMayBeStatic
    def is_holiday(self, predictiondate):
        db = Common.conn()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM T_HOLIDAY \
                         WHERE sitecode = '" + Common.sitecode + "' AND Holiday = '" + predictiondate + "' ")
        holiday = cursor.fetchall()
        holiday_cnt = holiday[0][0]

        if holiday_cnt == 1:
            isholiday = 'Y'
        else:
            isholiday = 'N'
        cursor.close()
        db.close()
        return isholiday

    # 15분 단위 피크전력 예측에 대한 전력값 저장
    # noinspection PyMethodMayBeStatic
    def insert_powerprediction15(self, df_row):
        date_time = df_row['date'] + ' ' + str(df_row['hour']) + ':' + str(df_row['min'])
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT COUNT(*) FROM T_POWER_PREDICT_15M \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                    AND BuildingNo = '" + b_no + "' \
                    AND PredictDate = '" + str(df_row['date']) + "' \
                    AND PredictHour = '" + str(df_row['hour']) + "' \
                    AND PredictMin = '" + str(df_row['min']) + "' "

        cursor.execute(sql)
        all_row = cursor.fetchall()
        count = all_row[0][0]

        if count < 1:
            sql = "INSERT INTO T_POWER_PREDICT_15M(SiteCode, BuildingNo, EnergySource, \
                   PredictDate, PredictHour, PredictMin, RealPower15M, PredictPower15M, WeekHoliday) \
                   VALUES(%s, %s, %d, %s, %s, %s, %d, %d, %d) "
            val = (Common.sitecode, b_no, str(df_row['energysource']), str(df_row['date']), str(df_row['hour']),
                   str(df_row['min']), df_row['realpower'], df_row['predictpower'], str(df_row['weekholiday']))
            #      str(df_row['min']), df_row['realpower'].item(), df_row['predictpower'].item(), str(df_row['weekholiday']))

            cursor.execute(sql, val)
            db.commit()

        else:
            sql = " UPDATE T_POWER_PREDICT_15M \
                       SET RealPower15M = %d \
                          ,PredictPower15M = %d \
                     WHERE SITECODE = '" + Common.sitecode + "' \
                       AND BuildingNo = '" + b_no + "' \
                       AND EnergySource = '" + str(df_row['energysource']) + "' \
                       AND PredictDate = '" + str(df_row['date']) + "' \
                       AND PredictHour = '" + str(df_row['hour']) + "' \
                       AND PredictMin = '" + str(df_row['min']) + "' "
            val = (df_row['realpower'], df_row['predictpower'])
            # val = (df_row['realpower'].item(), df_row['predictpower'].item())
            cursor.execute(sql, val)
            db.commit()
        cursor.close()
        db.close()
        return

    # noinspection PyMethodMayBeStatic
    def insert_powerprediction_hourly(self, df_row):
        db = Common.conn()
        cursor = db.cursor()
        sql = " SELECT BuildingNo, MainEnergySource \
                  FROM T_BUILDING_INFO WHERE SITECODE = '" + Common.sitecode + "' "
        cursor.execute(sql)
        all_row = cursor.fetchall()
        bno = all_row[0][0]
        energy_src = all_row[0][1]

        sql = " SELECT COUNT(*) FROM T_POWER_PREDICT_HOURLY \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                    AND BuildingNo = '" + bno + "' \
                    AND PredictDate = '" + df_row['date'] + "' \
                    AND PredictHour = '" + df_row['hour'] + "' \
                    AND EnergySource = '" + str(energy_src) + "' "
        cursor.execute(sql)
        all_row = cursor.fetchall()
        count = all_row[0][0]

        if count < 1:
            sql = "INSERT INTO T_POWER_PREDICT_HOURLY(SiteCode, BuildingNo, PredictDate, PredictHour, \
                                                      PredictPower, WeekHoliday, EnergySource) \
                   VALUES(%s, %s, %s, %s, %d, %s, %s) "
            val = (Common.sitecode, bno, df_row['date'], df_row['hour'],
                   df_row['predictpower'], str(df_row['weekholiday']), str(energy_src))
            cursor.execute(sql, val)
            db.commit()

        else:
            sql = " UPDATE T_POWER_PREDICT_HOURLY \
                       SET PredictPower = %d \
                          ,WeekHoliday = %d \
                     WHERE SITECODE = '" + Common.sitecode + "' \
                       AND BuildingNo = '" + bno + "' \
                       AND PredictDate = '" + df_row['date'] + "' \
                       AND PredictHour = '" + df_row['hour'] + "' \
                       AND EnergySource = '" + str(energy_src) + "' "
            val = (df_row['predictpower'], str(df_row['weekholiday']))
            cursor.execute(sql, val)
            db.commit()
        cursor.close()
        db.close()
        return

    # 노점온도 및 습구온도 계산 함수
    # noinspection PyMethodMayBeStatic
    def calculation_dew_wet_temp(self, temp, reh):
        dew_temp = 238.88 * (np.log(reh / 100) + 17.358 * temp / (238.88 + temp)) / \
                   (17.358 - (np.log(reh / 100) + 17.358 * temp / (238.88 + temp)))

        wet_temp = temp * (np.arctan(0.151977 * (reh + 8.313659) ** 0.5) + np.arctan(temp + reh) -
                           np.arctan(reh - 1.676331)) + (0.00391838 * reh ** 1.5) * np.arctan(0.023101 * reh) - 4.686035

        df_dew_wet = pd.DataFrame(columns=['Dew_temp', 'Wet_temp'])
        df_dew_wet['Dew_temp'] = dew_temp
        df_dew_wet['Wet_temp'] = wet_temp
        return df_dew_wet

    # 기상 민감도 생성 함수(15분 예측)
    # noinspection PyMethodMayBeStatic
    def sensitivity_generation_15m(self, df_sense_power, predict_hour):
        df_sense_power['Const'] = 1  # 상수항
        Y = df_sense_power[(df_sense_power['Hour'] == predict_hour)][['RealPower15M']].to_numpy()
        X = df_sense_power[(df_sense_power['Hour'] == predict_hour)][['Temp', 'Reh', 'Wet_temp']].to_numpy()

        w = np.linalg.inv(X.T @ X) @ X.T @ Y
        # w = np.linalg.inv(X.T @ X) @ X.T @ Y
        mse_wet = (Y - X @ w).T @ (Y - X @ w) / len(Y)

        X = df_sense_power[(df_sense_power['Hour'] == predict_hour)][['Temp', 'Reh', 'Dew_temp']].to_numpy()

        w = np.linalg.inv(X.T @ X) @ X.T @ Y
        mse_dew = (Y - X @ w).T @ (Y - X @ w) / len(Y)

        if mse_wet[0] <= mse_dew[0]:
            sensitivity_type = 1
        else:
            sensitivity_type = 2

        df_sensitivity = pd.DataFrame(columns=['Hour', 'Coefficient1', 'Coefficient2', 'Coefficient3'])
        hour_list = df_sense_power['Hour'].unique()

        df_sense_power['const'] = 1  # 상수항

        if sensitivity_type == 1:
            X_attributes = ['Const', 'Temp', 'Reh', 'Wet_temp']
        else:
            X_attributes = ['Const', 'Temp', 'Reh', 'Dew_temp']

        sens_cnt = 0
        for hour_no in hour_list:
            X = df_sense_power[(df_sense_power['Hour'] == hour_no)][X_attributes].to_numpy()
            Y = df_sense_power[(df_sense_power['Hour'] == hour_no)][['RealPower15M']].to_numpy()
            w = np.linalg.inv(X.T @ X) @ X.T @ Y
            df_sensitivity.loc[sens_cnt] = [hour_no, w[1, 0], w[2, 0], w[3, 0]]
            sens_cnt = sens_cnt + 1

        del df_sense_power, X, Y
        return df_sensitivity

    # 기상 민감도 생성 함수(1시간 예측)
    # noinspection PyMethodMayBeStatic
    def sensitivity_generation_hourly(self, df_sense_power, predict_hour, holiday):
        df_sense_power['const'] = 1  # 상수항
        Y = df_sense_power[(df_sense_power['WeekHoliday'] == holiday) & \
                           (df_sense_power['Hour'] == predict_hour)][['RealPower15M']].to_numpy()
        X = df_sense_power[(df_sense_power['WeekHoliday'] == holiday) & \
                           (df_sense_power['Hour'] == predict_hour)][['const', 'Temp', 'Reh', 'Wet_temp']].to_numpy()

        w = np.linalg.inv(X.T @ X) @ X.T @ Y
        mse_wet = (Y - X @ w).T @ (Y - X @ w) / len(Y)

        X = df_sense_power[(df_sense_power['WeekHoliday'] == holiday) & \
                           (df_sense_power['Hour'] == predict_hour)][['const', 'Temp', 'Reh', 'Dew_temp']].to_numpy()
        w = np.linalg.inv(X.T @ X) @ X.T @ Y
        mse_dew = (Y - X @ w).T @ (Y - X @ w) / len(Y)

        if mse_wet[0, 0] <= mse_dew[0, 0]:
            sensitivity_type = 1
        else:
            sensitivity_type = 2

        df_sensitivity = pd.DataFrame(columns=['WeekHoliday', 'Hour', 'Coefficient1', 'Coefficient2', 'Coefficient3'])
        holiday_list = df_sense_power['WeekHoliday'].unique()
        hour_list = df_sense_power['Hour'].unique()

        df_sense_power['const'] = 1  # 상수항

        if sensitivity_type == 1:
            X_attributes = ['const', 'Temp', 'Reh', 'Wet_temp']
        else:
            X_attributes = ['const', 'Temp', 'Reh', 'Dew_temp']

        sens_cnt = 0
        for holiday_no in holiday_list:
            for hour_no in hour_list:
                X = df_sense_power[(df_sense_power['WeekHoliday'] == holiday_no) & \
                                   (df_sense_power['Hour'] == hour_no)][X_attributes].to_numpy()
                Y = df_sense_power[(df_sense_power['WeekHoliday'] == holiday_no) & \
                                   (df_sense_power['Hour'] == hour_no)][['RealPower15M']].to_numpy()
                w = np.linalg.inv(X.T @ X) @ X.T @ Y
                df_sensitivity.loc[sens_cnt] = [holiday_no, hour_no, w[1, 0], w[2, 0], w[3, 0]]
                sens_cnt = sens_cnt + 1

        del df_sense_power, X, Y
        # gc.collect()
        return df_sensitivity

    # 기상정보 클러스터링 함수
    # noinspection PyMethodMayBeStatic
    def climate_clustering(self, X_cluster):
        X_cluster_scaled = MinMaxScaler().fit_transform(X_cluster)

        # 클러스터링 갯수들을 리스트로 받아서, 각 갯수별로 클러스터링을 적용하고 실루엣 개수 구함
        df_cluster = pd.DataFrame(columns=['cluster_no', 'cluster_labels'])

        inertia = []

        for n_cluster in range(3, 9):
            df_cluster_imsi = pd.DataFrame(columns=['cluster_no', 'cluster_labels'])

            # 기상정보 KMeans 클러스터링 수행
            clusterer = KMeans(n_clusters=n_cluster, init='k-means++', max_iter=500, random_state=42)
            clusterer.fit(X_cluster_scaled)

            # inertia : 중심점으로부터의 거리의 합으로 클러스터의 응집도를 나타냄
            inertia.append(clusterer.inertia_)

            cluster_labels = clusterer.predict(X_cluster_scaled)

            df_cluster_imsi['cluster_labels'] = cluster_labels
            df_cluster_imsi['cluster_no'] = n_cluster
            df_cluster = pd.concat([df_cluster, df_cluster_imsi])

        max_cluster = 0
        max_inertia = 0

        for j in range(4, 8):
            inertia_slope = np.abs(inertia[j - 4] - 2 * inertia[j - 3] + inertia[j - 2])
            if inertia_slope > max_inertia:
                max_cluster = j
                max_inertia = inertia_slope

        # 기울기 변화가 최대인 클러스터 값
        df_cluster = df_cluster[(df_cluster['cluster_no'] == max_cluster)][['cluster_labels']]
        # kl = KneeLocator(range(1, 7), inertia, curve="convex", direction="decreasing")
        # 최적 클러스터 유형
        # df_cluster = df_cluster[(df_cluster['cluster_no'] == kl.elbow)][['cluster_labels']]

        del X_cluster, X_cluster_scaled, df_cluster_imsi, clusterer
        # gc.collect()
        return df_cluster

    # 습구온도 클러스터링 함수
    # noinspection PyMethodMayBeStatic
    def temp_clustering_1hour(self, df_date, X_cluster):
        df_cluster = pd.DataFrame(columns=['Date', 'Cluster_no', 'Temp_cluster'])
        df_cluster['Date'] = pd.to_datetime(df_cluster['Date'], format="%Y-%m-%d")

        inertia = []

        for n_cluster in range(3, 9):
            df_cluster_imsi = pd.DataFrame(columns=['Date', 'Cluster_no', 'Temp_cluster'])

            # 습구온도 KShape 클러스터링 수행
            kshape = KShape(n_clusters=n_cluster, verbose=0, max_iter=100, random_state=42)
            kshape.fit(X_cluster)

            # inertia : 중심점으로부터의 거리의 합으로 클러스터의 응집도를 나타냄
            inertia.append(kshape.inertia_)

            cluster_labels = kshape.predict(X_cluster)

            df_cluster_imsi['Date'] = df_date
            df_cluster_imsi['Cluster_no'] = n_cluster
            df_cluster_imsi['Temp_cluster'] = cluster_labels
            df_cluster = pd.concat([df_cluster, df_cluster_imsi])

        max_cluster = 0
        max_inertia = 0

        for j in range(4, 8):
            inertia_slope = np.abs(inertia[j - 4] - 2 * inertia[j - 3] + inertia[j - 2])
            if inertia_slope > max_inertia:
                max_cluster = j
                max_inertia = inertia_slope

        # 기울기 변화가 최대인 클러스터 값
        df_cluster = df_cluster[(df_cluster['Cluster_no'] == max_cluster)][['Date', 'Temp_cluster']]
        # kl = KneeLocator(range(1, 7), inertia, curve="convex", direction="decreasing")
        # df_cluster = df_cluster[(df_cluster['Cluster_no'] == kl.elbow)][['Date', 'Temp_cluster']]

        del df_cluster_imsi, kshape
        # gc.collect()
        return df_cluster

    # 습구온도 클러스터링 함수
    # noinspection PyMethodMayBeStatic
    def temp_clustering_15min(self, df_date, X_cluster):
        df_cluster = pd.DataFrame(columns=['Serial_no', 'Cluster_no', 'Wettemp_cluster'])

        inertia = []

        for n_cluster in range(3, 9):
            df_cluster_imsi = pd.DataFrame(columns=['Serial_no', 'Cluster_no', 'Wettemp_cluster'])

            # 습구온도 KShape 클러스터링 수행
            kshape = KShape(n_clusters=n_cluster, verbose=0, max_iter=100, random_state=42)
            kshape.fit(X_cluster)

            # inertia : 중심점으로부터의 거리의 합으로 클러스터의 응집도를 나타냄
            inertia.append(kshape.inertia_)

            cluster_labels = kshape.predict(X_cluster)

            df_cluster_imsi['Serial_no'] = df_date
            df_cluster_imsi['Cluster_no'] = n_cluster
            df_cluster_imsi['Wettemp_cluster'] = cluster_labels
            df_cluster = pd.concat([df_cluster, df_cluster_imsi])

        max_cluster = 0
        max_inertia = 0

        for j in range(4, 8):
            inertia_slope = np.abs(inertia[j - 4] - 2 * inertia[j - 3] + inertia[j - 2])
            if inertia_slope > max_inertia:
                max_cluster = j
                max_inertia = inertia_slope

        # 기울기 변화가 최대인 클러스터 값
        df_cluster = df_cluster[(df_cluster['Cluster_no'] == max_cluster)][['Serial_no', 'Wettemp_cluster']]

        del df_cluster_imsi, kshape
        # gc.collect()
        return df_cluster

    # noinspection PyMethodMayBeStatic
    def modification_week_date(self, predict_date):
        db = Common.conn()
        cursor = db.cursor()
        sql = "SELECT distinct TOP 7 r.RealDate \
                 FROM T_POWER_REAL_15M r \
                WHERE r.SiteCode =  '" + Common.sitecode + "' \
                  AND r.RealDate < '" + predict_date + "' \
                  AND r.WeekHoliday = 1 \
                 ORDER BY r.RealDate DESC "
        """
        sql = "SELECT distinct TOP 7 Convert(varchar(10), r.SaveTime,112) \
                 FROM T_POWER_REAL_15M r \
                WHERE r.SiteCode =  '" + Common.sitecode + "' \
                  AND Convert(varchar(10), r.SaveTime,112) < '" + predict_date + "' \
                  AND r.WeekHoliday = 1 \
                 ORDER BY Convert(varchar(10), r.SaveTime,112) DESC "
        """

        # 실행문 조회
        m_date = pd.read_sql(sql, db)
        cursor.close()
        db.close()
        return m_date.values

    # 최근 일주일 간의 평일의 각 실측전력과 예측전력을 구하고 실측전력/예측전력으로
    # 보정 계수를 계산
    # noinspection PyMethodMayBeStatic
    """
    def modification_factor_hour(self, predictdate, n_hour):

        hour = int(n_hour) // 100
        hour = str(hour)

        db = Common.conn()
        cursor = db.cursor()
        sql = "    SELECT CASE WHEN p.P_Power = 0 THEN 1 \
                                ELSE r.Power/p.P_Power END AS Revision \
                     FROM (\
                           SELECT ISNULL(SUM(r.RealPower15M), 0) Power \
                             FROM T_POWER_REAL_15M r \
                                 ,( SELECT distinct TOP 7 r.RealDate AS d_date \
                                          FROM T_POWER_REAL_15M r \
                                         WHERE r.SiteCode = '" + Common.sitecode + "' \
                                           AND r.RealDate < '" + predictdate + "' \
                                           AND r.WeekHoliday = 1 \
                                          ORDER BY r.RealDate DESC \
                                       ) d \
                            WHERE r.SiteCode = '" + Common.sitecode + "' \
                              AND r.RealPower15M > 0 \
                              AND r.RealHour = '" + hour + "' \
                              AND r.WeekHoliday = 1 \
                              AND r.RealDate = d.d_date \
                         ) r \
                        ,( \
                          SELECT ISNULL(SUM(p.PredictPower), 0) AS P_Power \
                             FROM T_POWER_PREDICT_HOURLY p \
                            WHERE p.SiteCode = '" + Common.sitecode + "' \
                              AND p.PredictPower > 0 \
                             AND p.WeekHoliday = 1 \
                              AND p.PredictHour = '" + n_hour + "' \
                              AND p.PredictDate IN \
                                     ( SELECT distinct TOP 7 p.PredictDate \
                                         FROM T_POWER_PREDICT_HOURLY p \
                                        WHERE p.SiteCode = '" + Common.sitecode + "' \
                                          AND p.PredictDate < '" + predictdate + "' \
                                          AND p.WeekHoliday = 1 \
                                       ORDER BY p.PredictDate DESC \
                                     ) \
                         ) p "

        cursor.execute(sql)

        factor = cursor.fetchall()
        m_factor = factor[0][0]
        # df_power = pd.read_sql(sql, db)
        # r_power = df_power.values[0][0]
        # p_power = df_power.values[0][1]
        # if p_power == 0:
        #     m_factor = 1
        # else:
        #     m_factor = r_power/p_power
        cursor.close()
        db.close()
        return round(m_factor, 2)

    # 최근 일주일 간의 평일의 각 실측전력과 예측전력을 구하고 실측전력/예측전력으로
    # 보정 계수를 계산
    # noinspection PyMethodMayBeStatic
    def modification_factor_15m(self, predictdate, n_hour, n_min):

        predict_date = predictdate + " " + str(n_hour) + ":" + str(n_min)
        print("predict_date:", predict_date)

        db = Common.conn()
        cursor = db.cursor()
        sql = "    SELECT CASE WHEN p.P_Power = 0 THEN 1 \
                                ELSE r.Power/p.P_Power END AS Revision \
                     FROM \
                         ( \
                          SELECT ISNULL(SUM(r.RealPower15M), 0) Power \
                             FROM T_POWER_REAL_15M r \
                            WHERE r.SiteCode = '" + Common.sitecode + "' \
                              AND r.RealPower15M > 0 \
                              AND r.RealDate < '" + predict_date + "' \
                              AND r.RealDate >= DATEADD(hour, -1, '" + predict_date + "') \
                            ) r \
                       ,( \
                          SELECT ISNULL(SUM(p.PredictPower15M), 0) AS P_Power \
                             FROM T_POWER_PREDICT_15M p \
                            WHERE p.SiteCode = '" + Common.sitecode + "' \
                              AND p.PredictPower15M > 0 \
                              AND Convert(VARCHAR(16), p.PredictDateTime,120) < '" + predict_date + "' \
                              AND Convert(VARCHAR(16), p.PredictDateTime,120) >= \
                                  DATEADD(hour, -1, '" + predict_date + "') \
                         ) p "

        cursor.execute(sql)

        factor = cursor.fetchall()
        m_factor = factor[0][0]

        cursor.close()
        db.close()
        return round(m_factor, 2)
    """

    # noinspection PyMethodMayBeStatic
    def select_power_real_15m_date(self):
        db = Common.conn()
        cursor = db.cursor()
        sql = " SELECT MIN(RealDate) AS sdate, \
                       MAX(RealDate) AS edate \
                  FROM T_POWER_REAL_15M "
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        startdate = all_fetch[0][0]
        enddate = all_fetch[0][1]

        cursor.close()
        db.close()
        return startdate, enddate

    # noinspection PyMethodMayBeStatic
    def select_power_peak_info(self):
        db = Common.conn()
        cursor = db.cursor()

        sql = " SELECT BuildingNo, MMIEquipmentID \
                  FROM T_POWER_PEAK_INFO \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND EnergySource IN (1, 2) "

        power_peak_save = pd.read_sql(sql, db)
        cursor.close()
        db.close()
        return power_peak_save.values, power_peak_save.size

    # noinspection PyMethodMayBeStatic
    def select_building_no(self):
        db = Common.conn()
        cursor = db.cursor()

        sql = " SELECT BuildingNo \
                  FROM T_BUILDING_INFO \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND MainYN = 'Y' \
                   AND MainEnergySource IN (1, 2) "

        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        building_no = all_fetch[0][0]

        # buildingno = [buildingno[0] for buildingno in cursor.fetchall()]
        """
        building_no = "("
        for bno in buildingno:
            building_no += "'"+bno + "',"
        building_no = building_no[:-1] + ")"
        """
        cursor.close()
        db.close()
        return building_no

    # energy_source, mmi_id 별 15분 전력량 생성을 위한 energy_source, mmi_id 검색
    # noinspection PyMethodMayBeStatic
    def select_mmiid_esrc(self):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT MMIEquipmentID, EnergySource \
                  FROM T_POWER_PEAK_INFO \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' "

        df_mmiid_esrc = pd.read_sql(sql, db)
        mmiequipmentid_list = df_mmiid_esrc[['MMIEquipmentID', 'EnergySource']].values

        """
        mmiequipmentid = [mmiequipmentid[0] for mmiequipmentid in cursor.fetchall()]
        mmiequipment_id = "("
        for mmi_id in mmiequipmentid:
            mmiequipment_id += "'"+mmi_id + "',"
        mmiequipment_id = mmiequipment_id[:-1] + ")"
        """
        cursor.close()
        db.close()
        return mmiequipmentid_list

    # energy_source별 15분 전력량 예측을 위한 energy_source 검색
    # noinspection PyMethodMayBeStatic
    def select_energy_src(self):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT DISTINCT EnergySource \
                  FROM T_POWER_PEAK_INFO \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' "

        df_e_src = pd.read_sql(sql, db)
        esrc_list = df_e_src['EnergySource'].values

        cursor.close()
        db.close()
        return esrc_list

    """
    # noinspection PyMethodMayBeStatic
    def select_energysource(self, mmiequipmentid):
        db = Common.conn()
        cursor = db.cursor()
        bno = Common.select_building_no(self)

        sql = " SELECT EnergySource \
                  FROM T_POWER_PEAK_INFO \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + bno + "' \
                   AND MMIEquipmentID = '" + mmiequipmentid + "' "
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        EnergySource = all_fetch[0][0]

        cursor.close()
        db.close()
        return EnergySource
    """

    # noinspection PyMethodMayBeStatic
    def select_peak_power(self, mmi_id, next_time, next5_time):

        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)
        sql = " SELECT isnull(savetime,'0'), isnull(CurrentPowerKw,0), isnull(PowerKwInc, 0) \
                  FROM T_POWER_PEAK_SAVE \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND MMIEquipmentID = '" + mmi_id + "' \
                   AND Convert(VARCHAR(23), SaveTime,20) >= '" + next_time + "' \
                   AND Convert(VARCHAR(23), SaveTime,20) < '" + next5_time + "' "

        # 실행문 조회
        cursor.execute(sql)
        all_fetch = cursor.fetchall()

        if all_fetch == []:
            savetime = 0
            CurrentPowerKw = 0
            PowerKwInc = 0
        else:
            savetime = all_fetch[0][0]
            CurrentPowerKw = all_fetch[0][1]
            PowerKwInc = all_fetch[0][2]

        cursor.close()
        db.close()
        return savetime, CurrentPowerKw, PowerKwInc

    # 15분 전력 테이블 조회
    # noinspection PyMethodMayBeStatic
    def select_last_real_power(self, energy_source):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)
        sql = " SELECT isnull(MAX(RealDate + RealHour + RealMin), '19000101000000') AS max_date \
                  FROM T_POWER_REAL_15M \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' "

        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        last_date = all_fetch[0]

        cursor.close()
        db.close()
        return last_date

    # 15분 전력 테이블 조회
    # noinspection PyMethodMayBeStatic
    def select_real_power(self, energy_source, current_time):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)
        sql = " SELECT CurrentPowerKw, RealPower15M \
                  FROM T_POWER_REAL_15M \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND CONCAT(LEFT(RealDate, 4), '-', SUBSTRING(RealDate,5, 2), '-', RIGHT(RealDate,2), " \
                                       "' ', LEFT(RealHour,2), ':', RealMin, ':00') = '" + current_time + "' "

        # 실행문 조회
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        if all_fetch == []:
            CurrentPowerKw = 0
            RealPower15M = 0
        else:
            CurrentPowerKw = all_fetch[0][0]
            RealPower15M = all_fetch[0][1]
        cursor.close()
        db.close()
        return CurrentPowerKw, RealPower15M

    # noinspection PyMethodMayBeStatic
    def sum_predictpower15m_hourly(self, energy_source, start_date, end_date):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = "  SELECT ISNULL(SUM(PredictPower15M), 0) \
                   FROM T_POWER_PREDICT_15M \
                  WHERE SiteCode = '" + Common.sitecode + "' \
                    AND BuildingNo = '" + b_no + "' \
                    AND EnergySource = '" + str(energy_source) + "' \
                    AND CONVERT(VARCHAR(19), (PredictDate+LEFT(PredictHour,2)+PredictMin), 20) \
                                    BETWEEN '" + start_date + "' AND '" + end_date + "' "

        # print("sql:\n", sql)
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        sum_predictpower15m = all_fetch[0][0]

        cursor.close()
        db.close()
        return sum_predictpower15m


    # noinspection PyMethodMayBeStatic
    def sum_real_1hour_power(self, energy_source, start_date, end_date):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = "  SELECT ISNULL(SUM(RealPower15M), 0) \
                   FROM T_POWER_REAL_15M \
                  WHERE SiteCode = '" + Common.sitecode + "' \
                    AND BuildingNo = '" + b_no + "' \
                    AND EnergySource = '" + str(energy_source) + "' \
                    AND CONVERT(VARCHAR(19), (RealDate+LEFT(RealHour,2)+RealMin), 20) \
                                    BETWEEN '" + start_date + "' AND '" + end_date + "' "

        # print("sql:\n", sql)
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        sum_real_1hour_power = all_fetch[0][0]

        cursor.close()
        db.close()
        return sum_real_1hour_power


    # 15분 전력량 데이터에서 시각과 분이 같은 휴일 데이터 가져오기
    # noinspection PyMethodMayBeStatic
    def holiday_real_power(self, realdate, real_hour_min):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = "  SELECT TOP 1 RealPower15M \
                   FROM T_POWER_REAL_15M \
                  WHERE SiteCode = '" + Common.sitecode + "' \
                    AND BuildingNo = '" + b_no + "' \
                    AND WeekHoliday = 0 \
                    AND RealDate < '" + realdate + "' \
                    AND Convert(CHAR(8), CONCAT(left(RealHour,2), ':', CONCAT(RealMin,':00'), 24)) = '" + real_hour_min + "' \
                  ORDER BY SaveTime DESC "

    # 실행문 조회
        cursor.execute(sql)
        all_fetch = cursor.fetchall()
        if all_fetch == []:
            RealPower15M = 0
        else:
            RealPower15M = all_fetch[0]
        cursor.close()
        db.close()
        return RealPower15M

        # noinspection PyMethodMayBeStatic

    # 순전력량과 누적차이 계산 함수
    # noinspection PyMethodMayBeStatic
    def net_power_calculation(self, accumpower1, accumpower2):
        # 16비트 전력량계가 reset 되는 경우
        if (accumpower1 <= 2 ** 16 - 1) & (accumpower1 > 2 ** 15) & ((accumpower1 - accumpower2) > 2 ** 15):
            net_power = 2 ** 16 - 1 - accumpower1 + accumpower2  # 순전력량
            power_diff = accumpower1 - (2 ** 16 - 1)  # 누적차이
        else:
            # 32비트 전력량계가 reset 되는 경우
            if (accumpower1 > 2 ** 31) & ((accumpower1 - accumpower2) > 2 ** 31):
                net_power = 2 ** 32 - 1 - accumpower1 + accumpower2  # 순전력량
                power_diff = accumpower1 - (2 ** 32 - 1)  # 누적차이
            else:
                net_power = accumpower2 - accumpower1  # 순전력량
                power_diff = accumpower1  # 누적차이
        return round(net_power, 3), power_diff

    # noinspection PyMethodMayBeStatic
    def select_CurrentPowerKw_power(self, energy_source, real_datetime):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT CurrentPowerKw FROM T_POWER_REAL_15M \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND RealDate = '" + real_datetime[0:8] + "' \
                   AND RealHour = '" + real_datetime[8:12] + "' \
                   AND RealMin = '" + real_datetime[12:14] + "' "

        # print("sql:", sql)
        cursor.execute(sql)
        all_row = cursor.fetchall()
        if all_row == []:
            CurrentPowerKw = 0
        else:
            CurrentPowerKw = all_row[0][0]
        cursor.close()
        db.close()
        return CurrentPowerKw


    # noinspection PyMethodMayBeStatic
    def select_real_15power(self, energy_source, real_datetime):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT RealPower15M FROM T_POWER_REAL_15M \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND RealDate = '" + real_datetime[0:8] + "' \
                   AND RealHour = '" + real_datetime[8:10] + "' + '00' \
                   AND RealMin = '" + real_datetime[10:12] + "' "

        # print("sql:", sql)
        cursor.execute(sql)
        all_row = cursor.fetchall()
        if all_row == []:
            RealPower15M = 0
        else:
            RealPower15M = all_row[0][0]
        # print("RealPower15M:",RealPower15M)
        cursor.close()
        db.close()
        return RealPower15M

    #   insert_power_real_15m(buildingno, e_src, current_date, accumulate_power, real_power, WeekHoliday)
    # noinspection PyMethodMayBeStatic
    def insert_power_real_15m(self, energy_source, realdate, realhour, realmin, CurrentPowerKw, RealPower15M, WeekHoliday):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT COUNT(*) FROM T_POWER_REAL_15M \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND RealDate = '" + realdate + "' \
                   AND RealHour = '" + realhour + "' \
                   AND RealMin = '" + realmin + "' "

        cursor.execute(sql)
        all_row = cursor.fetchall()
        count = all_row[0][0]

        if count == 0:
            sql = "INSERT INTO T_POWER_REAL_15M(SiteCode, BuildingNo, EnergySource, RealDate, RealHour, RealMin, \
                                                CurrentPowerKw, RealPower15M, WeekHoliday) \
                   VALUES(%s, %s, %d, %s, %s, %s, %d, %d, %d) "
            val = (Common.sitecode, b_no, int(energy_source), str(realdate), str(realhour), str(realmin),
                   CurrentPowerKw, RealPower15M, WeekHoliday)
            cursor.execute(sql, val)
            db.commit()
        else:
            sql = " UPDATE T_POWER_REAL_15M \
                       SET CurrentPowerKw = %d \
                          ,RealPower15M = %d \
                     WHERE SITECODE = '" + Common.sitecode + "' \
                       AND BuildingNo = '" + b_no + "' \
                       AND EnergySource = '" + energy_source + "' \
                       AND RealDate = '" + realdate + "' \
                       AND RealHour = '" + realhour + "' \
                       AND RealMin = '" + realmin + "' "
            val = (CurrentPowerKw, RealPower15M)
            cursor.execute(sql, val)
            db.commit()
        cursor.close()
        db.close()
        return

    # 15분 예측 전력수요량 테이블에 15분 실제 전력량 업데이트
    # noinspection PyMethodMayBeStatic
    def update_predict_real15mpower(self, energy_source, predictdate, predicthour, predictmin, real_power):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " SELECT COUNT(*) FROM T_POWER_PREDICT_15M \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND PredictDate = '" + predictdate + "' \
                   AND PredictHour = '" + predicthour + "' \
                   AND PredictMin = '" + predictmin + "' "
        # print("sql", sql)
        cursor.execute(sql)
        all_row = cursor.fetchall()
        count = all_row[0][0]
        # print("count", count)
        if count == 1:
            sql = " UPDATE T_POWER_PREDICT_15M \
                       SET RealPower15M = '" + str(real_power) + "' \
                     WHERE SITECODE = '" + Common.sitecode + "' \
                       AND BuildingNo = '" + b_no + "' \
                       AND EnergySource = '" + energy_source + "' \
                       AND PredictDate = '" + predictdate + "' \
                       AND PredictHour = '" + predicthour + "' \
                       AND PredictMin = '" + predictmin + "' "
            # print("sql", sql)
            cursor.execute(sql)
            db.commit()
        cursor.close()
        db.close()
        return

    # 15분 예측 전력수요량 테이블에 15분 실제 전력량 업데이트
    # noinspection PyMethodMayBeStatic
    def update_predict_real1hourpower(self, energy_source, predictdate, predicthour, real_1hour_power):
        db = Common.conn()
        cursor = db.cursor()
        b_no = Common.select_building_no(self)

        sql = " UPDATE T_POWER_PREDICT_HOURLY \
                   SET RealPower = '" + str(real_1hour_power) + "' \
                 WHERE SITECODE = '" + Common.sitecode + "' \
                   AND BuildingNo = '" + b_no + "' \
                   AND EnergySource = '" + energy_source + "' \
                   AND PredictDate = '" + predictdate + "' \
                   AND PredictHour = '" + predicthour + "' "
        # print("sql", sql)
        cursor.execute(sql)
        db.commit()

        cursor.close()
        db.close()
        return

    # noinspection PyMethodMayBeStatic
    def get_outlier(self, df=None, column=None, weight=None, min=None):
        # power에 해당하는 column 데이터만 추출, 1/4 분위와 3/4 분위 지점을 np.percentile로 구함.
        power = df[column]
        quantile_25 = np.percentile(power.values, 25)
        quantile_75 = np.percentile(power.values, 75)
        # IQR을 구하고, IQR에 1.5를 곱하여 최대값과 최소값 지점 구함.
        iqr = quantile_75 - quantile_25
        iqr_weight = iqr * weight
        lowest_val = quantile_25 - iqr_weight
        highest_val = quantile_75 + iqr_weight
        # 최대값 보다 크거나, 최소값 보다 작은 값을 아웃라이어로 설정하고 DataFrame index 반환.
        if min == 60:
            outlier_index = power[(power < lowest_val) | (power > highest_val) | (power < 2)].index
        elif min == 15:
            outlier_index = power[(power < lowest_val) | (power > highest_val) | (power == 0)].index
        return outlier_index

    # 전력량 클러스터링 함수
    # noinspection PyMethodMayBeStatic
    def power_clustering(self, df_serial, X_cluster):
        df_cluster = pd.DataFrame(columns=['serial_no', 'cluster_no', 'Power_cluster'])

        inertia = []

        for n_cluster in range(3, 9):
            df_cluster_imsi = pd.DataFrame(columns=['serial_no', 'cluster_no', 'Power_cluster'])

            # 전력량 KShape 클러스터링 수행
            kshape = KShape(n_clusters=n_cluster, verbose=0, max_iter=100, random_state=42)
            kshape.fit(X_cluster)

            # inertia : 중심점으로부터의 거리의 합으로 클러스터의 응집도를 나타냄
            inertia.append(kshape.inertia_)

            cluster_labels = kshape.predict(X_cluster)

            df_cluster_imsi['serial_no'] = df_serial
            df_cluster_imsi['cluster_no'] = n_cluster
            df_cluster_imsi['Power_cluster'] = cluster_labels
            df_cluster = pd.concat([df_cluster, df_cluster_imsi])
        """
        # 기울기 변화가 최대인 클러스터 값
        kl = KneeLocator(range(3, 9), inertia, curve="convex", direction="decreasing")
        print(kl.elbow)
        # 최적 클러스터 유형
        # df_cluster = df_cluster[(df_cluster['cluster_no'] == kl.elbow)][['serial_no', 'power_cluster']]
        """

        max_cluster = 0
        max_inertia = 0

        for j in range(4, 8):
            inertia_slope = np.abs(inertia[j - 4] - 2 * inertia[j - 3] + inertia[j - 2])
            if inertia_slope > max_inertia:
                max_cluster = j
                max_inertia = inertia_slope

        # 기울기 변화가 최대인 클러스터 값
        df_cluster = df_cluster[(df_cluster['cluster_no'] == max_cluster)][['serial_no', 'Power_cluster']]

        del df_cluster_imsi, kshape
        # gc.collect()
        return df_cluster

    # 15분 데이터 생성을 실행하는 함수
    """
    @staticmethod
    def execute_power_15m(real_datetime):
        print("15분 전력량 데이터 생성!")
        threading.Timer(90, make_power.make_power_15m(real_datetime).start())
    """

    # 실행 날짜 체크
    # noinspection PyMethodMayBeStatic
    def op_days(self, startday, endday):
        db = Common.conn()
        cursor = db.cursor()
        sql = " SELECT DISTINCT(RealDate) AS DATE \
                  FROM T_POWER_REAL_15M \
                 WHERE SiteCode = '" + Common.sitecode + "' \
                   AND RealDate >= '" + startday + "' \
                   AND RealDate <= '" + endday + "' \
                 ORDER BY DATE "
        """
        sql = " SELECT CONVEROPERATING_CONFIGT(VARCHAR(10), DATEADD(D, NUMBER, '" + startday + "'), 112) AS [DATE] \
                  FROM MASTER..SPT_VALUES \
                 WHERE TYPE = 'P' \
                   AND number <= DATEDIFF(D, '" + startday + "', '" + endday + "') "
        """
        op_days = pd.read_sql(sql, db)
        cursor.close()
        db.close()
        return op_days


sitecode = ''  # GGTMC042
c = Common(sitecode)
sitecode = c.site_code()
# print("sitecode:", sitecode)

"""
sum_real_1hour_power = c.sum_real_1hour_power(2, '202208020915', '202208021000')
print("sum_real_1hour_power:", sum_real_1hour_power)
count = c.count_power_real_15m(2, '202208012330', '202208020015')
print("count:", count)

df_real = c.select_power_real_15m(2)
print("df_real:\n", df_real)

esrc = c.select_energy_src()
print("esrc:", esrc)

buildingno = c.select_building_no()
print("buildingno:", buildingno)

df_mmiid_esrc = c.select_mmiid_esrc('M')
print("df_mmiid_esrc:", df_mmiid_esrc)

power_peak_info, ppi_cnt = c.select_power_peak_info()
print("power_peak_info:", power_peak_info, ppi_cnt)

m_factor = c.modification_factor_hour('20200315', '0900')
print("mfactor:", m_factor)

m_factor = c.modification_factor_15m('20200710', 9, 15)
print("mfactor:", m_factor)

startdate, enddate = c.power_real_15m_date()
print("startdate:", startdate, "enddate", enddate)

electirc_power = c.net_power_calculation(95.44, 163.4)
print("electirc_power:", electirc_power)

sum_predictpower15m = c.sum_predictpower15m_hourly('20200130', '10', '11')
print("sum_predictpower15m:", sum_predictpower15m)
"""
"""
df_15m = c.create_5mto15m('2022-03-31 23:59', '2022-05-01 00:32')
print("df_15m:\n", df_15m)
print("날짜:", df_15m.values[0][0], "시간:", df_15m.values[0][1], "전력량", df_15m.values[0][2], "증분", df_15m.values[0][3])

df_date = c.modification_week_date('20200315')
print("df_date:", df_date)

isholiday = c.is_holiday('20200410')
print("isholiday:", isholiday)

df_holiday = c.get_holiday('20200106','20210118')
print("df_holiday:", df_holiday)

workstarttime, workstoptime = c.wokr_time()
print("workstarttime:", workstarttime, "workstoptime:", workstoptime)

power_sensing = c.power_sensing_value()
print("power_sensing:\n", power_sensing)

weather_predict = c.weather_predict_info()
print("weather_predict:\n", weather_predict)

weather_real = c.weather_real_info()
print("weather_real:\n", weather_real)
"""
