# power_predict_15m.py
# 15분 전력예측 방법 3 ~ 4, 주말 주초 및 기온민감도(1시간 단위)

from common_function import Common
from pandas import DataFrame
import pandas as pd
import numpy as np
import datetime as dt
import datetime
import time
import math
import gc
from downcast import reduce
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from bayes_opt import BayesianOptimization
from sklearn.ensemble import GradientBoostingRegressor as GBR
from lightgbm import LGBMRegressor as LGB
from xgboost import XGBRegressor as XGB
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from sklearn.datasets import fetch_openml
# from kneed import KneeLocator
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
mnist = fetch_openml('mnist_784', version=1, as_frame=False)

# p_date = "2020, 8, 5"
# p_time = "8, 45"

e_src = 2
p_year = 2022
p_month = 8
p_day = 2
p_hour = 12
p_min = 0


def PowerPrediction_15M(e_src, p_year, p_month, p_day, p_hour, p_min):

    random_seed = 42
    cnt = 0
    n = 0

    # 예측일시
    # predict_date = datetime.datetime(p_year, p_month, p_day)
    predictdate = dt.datetime(p_year, p_month, p_day)
    predict_time = dt.time(p_hour, p_min)

    predict_hour = predict_time.hour
    predict_min = predict_time.minute

    predicttomorrow = predictdate + datetime.timedelta(days=1)
    predict_tomorrow_hour = 0

    predictyesterday = predictdate - datetime.timedelta(days=1)

    predict_date = predictdate.strftime("%Y%m%d")
    predict_yesterday = predictyesterday.strftime("%Y%m%d")
    predict_tomorrow = predicttomorrow.strftime("%Y%m%d")

    startdate = predictdate - datetime.timedelta(days=30)
    start_date = startdate.strftime("%Y%m%d")

    # 데이터 가져오기
    workstarttime, workendtime = c.wokr_time()
    df_all_power = c.select_power_real_15m(e_src)
    df_all_real_weather = c.weather_real_info()
    df_all_predict_weather = c.weather_predict_info()

    df_all_power = reduce(df_all_power)
    # pd.set_option('display.max_columns', None)

    # 기상실황 노점온도 및 습구온도 속성 추가
    df_dew_wet = c.calculation_dew_wet_temp(df_all_real_weather['Temp'].values, df_all_real_weather['Reh'].values)
    df_all_real_weather[['Dew_temp', 'Wet_temp']] = df_dew_wet[['Dew_temp', 'Wet_temp']]

    # 기상예측 노점온도 및 습구온도 속성 추가
    df_dew_wet = c.calculation_dew_wet_temp(df_all_predict_weather['Temp'].values, df_all_predict_weather['Reh'].values)
    df_all_predict_weather[['Dew_temp', 'Wet_temp']] = df_dew_wet[['Dew_temp', 'Wet_temp']]

    df_all_real_weather['Hour'] = pd.to_numeric(df_all_real_weather['Hour'])
    df_all_predict_weather['Hour'] = pd.to_numeric(df_all_predict_weather['Hour'])

    #------------- 휴일 여부 데이터프레임 생성 시작 ---------------------
    df_holiday = pd.DataFrame(columns=['Date', 'WeekHoliday'])
    df_all_power = df_all_power.astype({'RealDate':'str'})
    df_before_holiday = df_all_power[(df_all_power['RealDate'] >= start_date) & (df_all_power['RealDate'] < predict_date)]
    df_holiday['Date'] = df_before_holiday['RealDate']
    df_holiday['WeekHoliday'] = df_before_holiday['WeekHoliday']
    df_holiday.drop_duplicates(['Date', 'WeekHoliday'], keep='first', inplace=True)
    df_holiday.reset_index(drop=True, inplace=True)

    holiday_cnt = len(df_holiday)
    holiday_code = c.get_holiday_day()

    for p_cnt in range(2):
        next_date = predictdate + datetime.timedelta(days=p_cnt)
        nextdate = next_date.strftime("%Y%m%d")
        isholiday = c.is_holiday(nextdate)

        if isholiday == 'Y':
            df_holiday.loc[holiday_cnt] = [nextdate, 0]
        else:
            if holiday_code == 7:
                if next_date.weekday() >= 5: # 월요일 = 0, ...., 일요일 = 6
                    df_holiday.loc[holiday_cnt] = [nextdate, 0]
                else:
                    df_holiday.loc[holiday_cnt] = [nextdate, 1]
            else:
                if holiday_code == next_date.weekday():
                    df_holiday.loc[holiday_cnt] = [nextdate, 0]
                else:
                    df_holiday.loc[holiday_cnt] = [nextdate, 1]
        holiday_cnt = holiday_cnt + 1
    #------------- 휴일 여부 데이터프레임 생성 끝 -----------------------

    if predict_hour == 0:
        predictyesterday = predictdate - datetime.timedelta(days=1)
        predict_yesterday = predictyesterday.strftime("%Y%m%d")
        holiday = df_holiday.loc[df_holiday['Date'] == predict_yesterday]['WeekHoliday'].values[0]
    else:
        holiday = df_holiday.loc[df_holiday['Date'] == predict_date]['WeekHoliday'].values[0]

    df_holiday.reset_index(drop=True, inplace=True)

    if holiday == 1:
        startdate = predictdate - datetime.timedelta(days=14)
    else:
        startdate = predictdate - datetime.timedelta(days=30)

    start_date = startdate.strftime("%Y%m%d")
    predictdate_nextday = (predictdate + datetime.timedelta(days=1)).strftime("%Y%m%d")
    df_holiday = df_holiday[df_holiday['Date'].between(start_date, predictdate_nextday)]
    df_holiday.reset_index(drop=True, inplace=True)

    # 일자 및 시간 속성 추가
    df_all_power['Savetime'] = pd.to_datetime(df_all_power['Savetime'])
    df_all_power['Date'] = df_all_power['Savetime'].dt.strftime("%Y%m%d")
    df_all_power['Hour'] = df_all_power['Savetime'].dt.hour
    df_all_power['Min'] = df_all_power['Savetime'].dt.minute

    df_all_power.loc[(df_all_power['Min'] > 0) & (df_all_power['Min'] < 15), 'Min'] = 15
    df_all_power.loc[(df_all_power['Min'] > 15) & (df_all_power['Min'] < 30), 'Min'] = 30
    df_all_power.loc[(df_all_power['Min'] > 30) & (df_all_power['Min'] < 45), 'Min'] = 45
    df_all_power.loc[(df_all_power['Min'] > 45), 'Min'] = 0
    df_all_power.drop(['RealDate', 'RealHour', 'RealMin', 'WeekHoliday', 'Savetime'], axis=1, inplace=True)

    # 시간별 근무 여부 데이터프레임
    df_work_hour = pd.DataFrame(columns=['Hour', 'Work'])

    # 근무시간에는 1, 근무시간 외에는 0
    for i in range(0, 24):
        if (i >= float(workstarttime)) & (i <= math.ceil(float(workendtime))):
            df_work_hour.loc[i] = [i, 1]
        else:
            df_work_hour.loc[i] = [i, 0]

    df_predict_power = pd.DataFrame(columns=['energysource', 'date', 'hour', 'min', 'realpower',
                                             'predictpower', 'weekholiday'])
    df_algorithm = pd.DataFrame(columns=['algorithm'])
    model_algo = []
    model_params = []

    start = time.time()

    # 날씨정보 가져오기
    df_real_weather1 = df_all_real_weather[(df_all_real_weather['Date'] >= start_date) &
                                           (df_all_real_weather['Date'] < predict_date)]
    df_real_weather2 = df_all_real_weather[(df_all_real_weather['Date'] == predict_date) &
                                           (df_all_real_weather['Hour'] < predict_hour)]
    if predict_hour < 23:
        if predict_min < 30:
            df_predict_weather = df_all_predict_weather[(df_all_predict_weather['Date'] == predict_date) &
                                                        (df_all_predict_weather['Hour'] >= predict_hour) &
                                                        (df_all_predict_weather['Hour'] <= predict_hour + 1)]
        else:
            df_predict_weather = df_all_predict_weather[(df_all_predict_weather['Date'] == predict_date) &
                                                        (df_all_predict_weather['Hour'] >= predict_hour) &
                                                        (df_all_predict_weather['Hour'] <= predict_hour + 2)]
    else:
        if predict_min < 30:
            df_predict_weather = df_all_predict_weather[((df_all_predict_weather['Date'] == predict_date) &
                                                         (df_all_predict_weather['Hour'] == predict_hour)) |
                                                        ((df_all_predict_weather['Date'] == predict_tomorrow) &
                                                         (df_all_predict_weather['Hour'] == predict_tomorrow_hour))]
        else:
            df_predict_weather = df_all_predict_weather[((df_all_predict_weather['Date'] == predict_date) &
                                                         (df_all_predict_weather['Hour'] == predict_hour)) |
                                                        ((df_all_predict_weather['Date'] == predict_tomorrow) &
                                                         (df_all_predict_weather['Hour'] <= predict_tomorrow_hour + 1))]

    df_weather = pd.concat([df_real_weather1, df_real_weather2, df_predict_weather])
    df_weather['Week'] = pd.to_datetime(df_weather['Date']).dt.weekday   #  + 1
    df_weather['Month'] = pd.to_datetime(df_weather['Date']).dt.month
    df_weather['Day'] = pd.to_datetime(df_weather['Date']).dt.day

    # holiday 속성 및 work 추가 및 정리
    df_weather = pd.merge(pd.merge(df_weather, df_holiday, on='Date'), df_work_hour, on='Hour')
    df_weather.loc[df_weather['WeekHoliday'] == 0, 'Work'] = 0
    df_weather = df_weather.sort_values(by=['Date', 'Hour'])

    # 과거 전력 데이터 가져오기
    df_past_power = df_all_power[((df_all_power['Date'] >= start_date) & (df_all_power['Date'] < predict_date)) |
                                 ((df_all_power['Date'] == predict_date) & (df_all_power['Hour'] < predict_hour)) |
                                 ((df_all_power['Date'] == predict_date) & (df_all_power['Hour'] == predict_hour) &
                                  (df_all_power['Min'] < predict_min))]

    df_past_power = df_past_power.sort_values(by=['Date', 'Hour', 'Min'])

    # 기온 민감도 산출을 위해 시간 간격 사용 전력량으로 15분 사용 전력량을 합함
    df_sense_power = df_past_power[(df_past_power['Date'] < predict_date) |
                                   ((df_past_power['Date'] == predict_date) & (df_past_power['Hour'] < predict_hour))]

    df_sense_power = df_sense_power.groupby(["Date", "Hour"], as_index=True).agg({'RealPower15M': 'sum'})
    df_sense_power.reset_index(inplace=True)
    past_power_max = df_sense_power['RealPower15M'].max()
    past_power_min = df_sense_power['RealPower15M'].min()

    # 과거 전력 데이터와 기상 데이터 병합
    df_past_power = pd.merge(df_past_power, df_weather, on=('Date', 'Hour'))
    df_sense_power = pd.merge(df_sense_power, df_weather, on=('Date', 'Hour'))

    # 과거 데이터 정리
    df_past_target = df_past_power['RealPower15M']
    df_past_min = df_past_power['Min']
    df_past_power = df_past_power.drop(['RealPower15M', 'Min'], axis=1)
    df_past_power['Min'] = df_past_min.values
    df_past_power['RealPower15M'] = df_past_target.values

    # 미래 데이터 생성
    for i in range(predict_min, 60 * (1 + predict_min // 30) + 1, 15):
        # print("i:", i, "i - 60 * (i // 60):", i - 60 * (i // 60))
        if i == predict_min:
            df_predict = df_weather[(df_weather['Date'] == predict_date) & (df_weather['Hour'] == predict_hour)]
            df_predict['Min'] = i
        else:
            if (predict_hour == 23) & (i >= 60):
                df_predict_imsi = \
                    df_weather[df_weather['Date'] == predict_tomorrow and df_weather['Hour'] == (i // 60) - 1]
                df_predict_imsi['Min'] = i - 60 * (i // 60)
                df_predict = pd.concat([df_predict, df_predict_imsi])
            else:
                df_predict_imsi = df_weather[(df_weather['Date'] == predict_date) &
                                             (df_weather['Hour'] == predict_hour + (i // 60))]
                df_predict_imsi['Min'] = i - 60 * (i // 60)
                df_predict = pd.concat([df_predict, df_predict_imsi])
    df_predict['RealPower15M'] = np.nan

    """
    # 성능 측정용 미래 전력 데이터 (테스트용으로 사용, 실제에서는 사용불가)
    if predict_hour < 23:
        Y_predict = df_all_power[(df_all_power['Date'] == predict_date) & (df_all_power['Hour'] == predict_hour) &
                                 (df_all_power['Min'] >= predict_min) |
                                 (df_all_power['Date'] == predict_date) & (df_all_power['Hour'] == predict_hour + 1) &
                                 (df_all_power['Min'] < predict_min))]['RealPower15M'].values
    else:
        Y_predict = df_all_power[(df_all_power['Date'] == predict_date) & (df_all_power['Hour'] == predict_hour) &
                                 (df_all_power['Min'] >= predict_min) |
                                 (df_all_power['Date'] == predict_tomorrow) & (df_all_power['Hour'] == 0) &
                                 (df_all_power['Min'] < predict_min)]['RealPower15M'].values
    """

    # 과거 데이터와 미래 데이터 통합
    df_total = pd.concat([df_past_power, df_predict])
    df_total.reset_index(drop=True, inplace=True)

    # 시차 피처 생성
    df_total['power_lag1'] = df_total['RealPower15M'].shift(1)
    df_total['power_lag2'] = df_total['RealPower15M'].shift(2)
    df_total['power_lag3'] = df_total['RealPower15M'].shift(3)
    df_total['power_lag4'] = df_total['RealPower15M'].shift(4)

    df_total['lag1'] = df_total['power_lag1']
    df_total['lag2'] = df_total['power_lag2']
    df_total['lag3'] = df_total['power_lag3']
    df_total['lag4'] = df_total['power_lag4']

    df_total.loc[df_total['power_lag1'] == 0, 'lag1'] = np.nan
    df_total.loc[df_total['power_lag2'] == 0, 'lag2'] = np.nan
    df_total.loc[df_total['power_lag3'] == 0, 'lag3'] = np.nan
    df_total.loc[df_total['power_lag4'] == 0, 'lag4'] = np.nan

    df_total['lag_mean'] = df_total[['lag1', 'lag2', 'lag3', 'lag4']].mean(axis=1)

    df_total['lag_changerate1'] = df_total['power_lag1'] / df_total['power_lag2']
    df_total['lag_changerate1'] = df_total['lag_changerate1'].replace([np.inf, -np.inf], np.nan).fillna(1)
    df_total['lag_changerate2'] = df_total['power_lag2'] / df_total['power_lag3']
    df_total['lag_changerate2'] = df_total['lag_changerate2'].replace([np.inf, -np.inf], np.nan).fillna(1)
    df_total['lag_changerate3'] = df_total['power_lag3'] / df_total['power_lag4']
    df_total['lag_changerate3'] = df_total['lag_changerate3'].replace([np.inf, -np.inf], np.nan).fillna(1)

    df_total = df_total.drop(['power_lag1', 'power_lag2', 'lag1', 'lag2', 'lag3', 'lag4'], axis=1)
    df_total = df_total.fillna(0)

    # 매시 0분 이외는 NULL 값으로 치환한 후 보간법으로 값 구하기
    df_total.loc[df_total['Min'] > 0, 'Temp'] = np.nan
    df_total['Temp'] = df_total['Temp'].interpolate()

    # 노점온도와 습구온도 다시 계산
    df_dew_wet = c.calculation_dew_wet_temp(df_total['Temp'].values, df_total['Reh'].values)
    df_total['Dew_temp'] = df_dew_wet['Dew_temp'].values
    df_total['Wet_temp'] = df_dew_wet['Wet_temp'].values

    # 시계열 데이터로 변환이 가능하게 일부 데이터 삭제
    time_series_cnt = 48
    df_total = df_total.iloc[len(df_total) % time_series_cnt:, :]
    df_total.reset_index(drop=True, inplace=True)
    df_total_index = df_total.index.values

    # lag_time 갯수만큼 제외
    # df_total = df_total.iloc[4:, :]

    # ------------------ 기상정보 K-Means 클러스터링 시작 ------------------------------------
    # 기상정보 클러스터링
    X_cluster = df_total[['Hour', 'WeekHoliday', 'Temp', 'Reh', 'Dew_temp', 'Wet_temp']].values
    df_cluster = c.climate_clustering(X_cluster)

    # 클러스터 값을 데이터프레임 cluster에 추가
    df_total['Climate_cluster'] = df_cluster.values
    # ------------------ 기상정보 K-Means 클러스터링 끝 -------------------------------------

    # ------------------ 습구온도 K-Shape 클러스터링 시작 --------------------------------------
    time_series_cnt = 48
    df_total = df_total.iloc[len(df_total) % time_series_cnt:, :]
    df_total.reset_index(drop=True, inplace=True)
    df_total_index = df_total.index.values

    df_total['Serial_no'] = df_total_index // time_series_cnt + 1

    df_serial = df_total['Serial_no'].unique()
    df_wettemp = df_total['Wet_temp']

    wettemp = df_wettemp.values.reshape((len(df_serial), time_series_cnt))

    wettemp_train = TimeSeriesScalerMeanVariance().fit_transform(wettemp)

    df_cluster = c.temp_clustering_15min(df_serial, wettemp_train)

    # 습구온도 클러스터 값을 속성으로 추가
    df_total = pd.merge(df_total, df_cluster, on=('Serial_no'))

    del df_total['Serial_no']
    # ------------------ 습구온도 K-Shape 클러스터링 끝 ----------------------------------------

    # ------------------ 전력량 K-Shape 클러스터링 시작 --------------------------------------
    df_total['serial_no'] = df_total_index // time_series_cnt + 1

    df_serial = df_total['serial_no'].unique()
    df_powerlag = df_total['lag_mean']

    powerlag = df_powerlag.values.reshape((len(df_serial), time_series_cnt))

    powerlag_train = TimeSeriesScalerMeanVariance().fit_transform(powerlag)
    df_cluster = c.power_clustering(df_serial, powerlag_train)

    # 전력량 클러스터 값을 속성으로 추가
    df_total = pd.merge(df_total, df_cluster, on=('serial_no'))
    del df_total['serial_no']
    # ------------------ 전력량 K-Shape 클러스터링 끝 --------------------------------------

    # 과거 데이터와 미래 데이터 분리 후 Holiday 체크
    df_past_power = df_total.iloc[:-len(df_predict), :]
    df_predict = df_total.iloc[-len(df_predict):, :]

    df_past_power = df_past_power[(df_past_power['WeekHoliday'] == holiday)]

    # 기상 민감도 속성
    if (df_sense_power.groupby(["Hour"]).size() > 1).all():
        df_sensitivity = c.sensitivity_generation_15m(df_sense_power, predict_hour)

    # 이상치 제거
    outlier_index_all = np.array([])
    hour_list = df_past_power['Hour'].unique()

    for hour_no in hour_list:
        df_hour = df_past_power[(df_past_power['Hour'] == hour_no)]
        outlier_index = c.get_outlier(df=df_hour, column='RealPower15M', weight=1.5, min=15)
        if len(outlier_index) > 0:
            outlier_index_all = np.append(outlier_index_all, outlier_index)
    df_past_power.drop(outlier_index_all, axis=0, inplace=True)

    # 이상치 제거 후
    df_real = df_past_power.sort_values(by=['Date', 'Hour', 'Min'])
    df_real_target = df_real['RealPower15M']
    df_real = df_real.drop('RealPower15M', axis=1)
    df_predict = df_predict.drop('RealPower15M', axis=1)

    # 시간별 전력 통계량(최소, 최대, 평균)
    df_past_power_stat = df_past_power.groupby(['Hour']).agg({'RealPower15M': ['min', 'max', 'mean']})
    df_past_power_stat.reset_index(inplace=True)

    # 전력량 통계량 속성 추가
    df_real = pd.merge(df_real, df_past_power_stat, on=('Hour'))
    df_predict = pd.merge(df_predict, df_past_power_stat, on=('Hour'))

    # 과거 데이터와 미래 데이터 통합
    df_total = pd.concat([df_real, df_predict])

    # 기상 민감도 속성 추가
    if len(df_sensitivity) > 0:
        df_total = pd.merge(df_total, df_sensitivity, on='Hour')
        df_total.sort_values(["Date", "Hour", "Min"], ascending=True, inplace=True)

    """
    writer = pd.ExcelWriter('./holiday(0524).xlsx', engine='xlsxwriter', datetime_format='yyyy-mm-dd')
    df_holiday.to_excel(writer, sheet_name='분별', index=False)
    writer.save()
    """

    # 원핫인코딩 후 과거와 미래 데이터 분리
    # df_dummy = pd.get_dummies(df_total, columns=['Hour', 'Min', 'Week', 'Work'])
    df_dummy = pd.get_dummies(df_total,
                       columns=['Hour', 'Min', 'Week', 'Climate_cluster', 'Wettemp_cluster', 'Power_cluster', 'Work'])
    df_dummy[['Hour', 'Min']] = df_total[['Hour', 'Min']]
    df_real_dummy = df_dummy.iloc[:-len(df_predict), :]
    df_predict_dummy = df_dummy.iloc[-len(df_predict):, :]

    # 입력 데이터와 목표 데이터 분리
    df_real_input = df_real_dummy.drop(['Date', 'Month', 'Day', 'Hour', 'Min'], axis=1)
    df_real_input['Hour'] = df_real_dummy['Hour']

    df_predict_time = df_predict_dummy[['Date', 'Hour', 'Min']]
    df_predict_input = df_predict_dummy.drop(['Date', 'Month', 'Day', 'Hour', 'Min'], axis=1)

    X = df_real_input.values
    Y = df_real_target.values
    X_predict = df_predict_input.values

    """
    # 가비지 컬렉션
    del df_past_power, df_sense_power, df_real, df_predict, df_total, df_cluster,\
        df_weather, df_real_weather1, df_real_weather2, df_predict_weather, df_sensitivity, \
        df_dew_wet, df_dummy, df_real_dummy, df_predict_dummy, X_cluster
    gc.collect()
    """

    # 학습 데이터와 시험 데이터 분리 및 훈련 데이터 더 추가
    for p in range(3):
        xTrainTemp, xTestTemp, yTrainTemp, yTestTemp = \
            train_test_split(X, Y, test_size=0.3, stratify=X[:, -1], random_state=42)
        if p == 0:
            X_train, X_test, Y_train, Y_test = xTrainTemp, xTestTemp, yTrainTemp, yTestTemp
        else:
            X_train = np.append(X_train, xTrainTemp, axis=0)
            X_test = np.append(X_test, xTestTemp, axis=0)
            Y_train = np.append(Y_train, yTrainTemp, axis=0)
            Y_test = np.append(Y_test, yTestTemp, axis=0)

    X_train = X_train[:, :-1]
    X_test = X_test[:, :-1]

    # 스케일링
    scaling = MinMaxScaler()
    scaling.fit(X_train)

    X_train_scaled = scaling.transform(X_train)
    X_test_scaled = scaling.transform(X_test)
    X_predict_scaled = scaling.transform(X_predict)

    """
    # 가비지 컬렉션
    del X_train, X_test, xTrainTemp, xTestTemp, yTrainTemp, yTestTemp
    gc.collect()
    """

    # 알고리즘 사전
    algorithm_dict = {
        0: 'GradientBoostingRegressor',
        1: 'XGBoostRegressor',
        2: 'LightGBMRegressor'
    }

    # 예측 결과 저장 데이터프레임
    output = pd.DataFrame(columns=['algo', 'mse', 'predictions', 'bestparams'])
    # print("X_predict_scaled:\n", X_predict_scaled)

    # 탐색 대상 함수 (GradientBoostingRegressor)
    def GBR_cv(max_depth, learning_rate, max_features, n_estimators):

        # 모델 정의
        model = GBR(max_depth=int(max_depth),
                    learning_rate=learning_rate,
                    max_features=int(max_features),
                    n_estimators=int(n_estimators)
                    )
        # 모델 훈련
        model.fit(X_train_scaled, Y_train)

        # 시험 예측값 출력
        Y_test_pred = model.predict(X_test_scaled)

        # 각종 metric 계산
        mse = mean_squared_error(Y_test, Y_test_pred)

        # 오차 최적화로 사용할 metric 반환
        return -mse

    # 실험해 보고자 하는 hyperparameter 집합
    gbr_bounds = {'max_depth': (2, 5),
                  'learning_rate': (0.01, 1.0),
                  'max_features': (3, 5),
                  'n_estimators': (50, 200)
                  }

    bo_gbr = BayesianOptimization(f=GBR_cv, pbounds=gbr_bounds, verbose=0, random_state=42)
    bo_gbr.maximize(init_points=2, n_iter=10, acq='ei', xi=0.01)

    # 파라미터 적용
    algo_model = GBR(max_depth=int(bo_gbr.max['params']['max_depth']),
                     learning_rate=bo_gbr.max['params']['learning_rate'],
                     max_features=int(bo_gbr.max['params']['max_features']),
                     n_estimators=int(bo_gbr.max['params']['n_estimators'])
                     )
    opt_model = algo_model.fit(X_train_scaled, Y_train)
    Y_pred = opt_model.predict(X_predict_scaled)

    output.loc[0] = [algorithm_dict.get(0), -bo_gbr.max['target'], Y_pred, bo_gbr.max['params']]

    # 탐색 대상 함수 (XGBoostRegressor)
    def XGB_cv(max_depth, learning_rate, n_estimators):

        # 모델 정의
        model = XGB(max_depth=int(max_depth),
                    learning_rate=learning_rate,
                    n_estimators=int(n_estimators)
                    )
        # 모델 훈련
        model.fit(X_train_scaled, Y_train)

        # 시험 예측값 출력
        Y_test_pred = model.predict(X_test_scaled)

        # 각종 metric 계산
        mse = mean_squared_error(Y_test, Y_test_pred)

        # 오차 최적화로 사용할 metric 반환
        return -mse

    # 실험해 보고자 하는 hyperparameter 집합
    xgb_bounds = {'max_depth': (2, 5),
                  'learning_rate': (0.01, 0.2),
                  'n_estimators': (20, 150)
                  }

    bo_xgb = BayesianOptimization(f=XGB_cv, pbounds=xgb_bounds, verbose=0, random_state=42)
    bo_xgb.maximize(init_points=2, n_iter=10, acq='ei', xi=0.01)

    # 파라미터 적용
    algo_model = XGB(max_depth=int(bo_xgb.max['params']['max_depth']),
                     learning_rate=bo_xgb.max['params']['learning_rate'],
                     n_estimators=int(bo_xgb.max['params']['n_estimators'])
                     )
    opt_model = algo_model.fit(X_train_scaled, Y_train)
    Y_pred = opt_model.predict(X_predict_scaled)

    output.loc[1] = [algorithm_dict.get(1), -bo_xgb.max['target'], Y_pred, bo_xgb.max['params']]

    # 탐색 대상 함수 (LightGBMRegressor)
    def LGB_cv(max_depth, learning_rate, n_estimators):

        # 모델 정의
        model = LGB(max_depth=int(max_depth),
                    learning_rate=learning_rate,
                    n_estimators=int(n_estimators)
                    )
        # 모델 훈련
        model.fit(X_train_scaled, Y_train)

        # 시험 예측값 출력
        Y_test_pred = model.predict(X_test_scaled)

        # 각종 metric 계산
        mse = mean_squared_error(Y_test, Y_test_pred)

        # 오차 최적화로 사용할 metric 반환
        return -mse

    # 실험해 보고자 하는 hyperparameter 집합
    lgb_bounds = {'max_depth': (2, 5),
                  'learning_rate': (0.01, 1.0),
                  'n_estimators': (50, 200)
                  }

    bo_lgb = BayesianOptimization(f=LGB_cv, pbounds=lgb_bounds, verbose=0, random_state=42)
    bo_lgb.maximize(init_points=2, n_iter=10, acq='ei', xi=0.01)

    # 파라미터 적용
    algo_model = LGB(max_depth=int(bo_lgb.max['params']['max_depth']),
                     learning_rate=bo_lgb.max['params']['learning_rate'],
                     n_estimators=int(bo_lgb.max['params']['n_estimators'])
                     )
    opt_model = algo_model.fit(X_train_scaled, Y_train)
    Y_pred = opt_model.predict(X_predict_scaled)

    output.loc[2] = [algorithm_dict.get(2), -bo_lgb.max['target'], Y_pred, bo_lgb.max['params']]

    """
    # 가비지 컬렉션
    del X_train_scaled, X_test_scaled, X_predict_scaled, bo_gbr, bo_xgb, bo_lgb, algo_model, opt_model
    gc.collect()
    """

    # 날짜 가져오기
    X_time = df_predict_time.values

    # 최적화 결과 mse가 작은 순으로 정렬 및 알고리즘, 초매개변수 저장
    output.sort_values(["mse"], ascending=True, inplace=True)
    model_algo = np.append(model_algo, output.iloc[0, 0])
    model_params = np.append(model_params, output.iloc[0, 3])

    # print("output.iloc[0, 2]:", output.iloc[0, 2])

    # 실제전력 및 예측전력 출력
    j = 0
    for i in output.iloc[0, 2]:
        # print("i:", i)
        if j > 3: break
        i = np.float64(i*0.8 + output.iloc[1,2][j]*0.2)
        # print("i:", i, "j:", j, "output.iloc[1,2][j]:", output.iloc[1,2][j])
        #i = np.float64(i)
        power_round = np.around(i)

        # 예측전력이 0보다 적은 경우 예측전력 0
        if power_round < 0:
            power_round = 0

        print("EnergySource %d " % e_src, "일자 %s  " % (X_time[j, 0]), "시간 %s  " % (str(X_time[j, 1])+'00'),
              "분 %s  " % (str(X_time[j, 2]).zfill(2)),
              "예측전력 %.2f  " % power_round, "휴일여부 %d" % holiday, "알고리즘 %s" % output.iloc[0, 0])

        df_predict_power.loc[cnt] = [e_src, str(X_time[j, 0]), str(X_time[j, 1])+'00',
                                     str(X_time[j, 2]).zfill(2), 0, power_round, holiday]
        # df_predict_power.loc[cnt] = [e_src,X_time[j,0],X_time[j,1],X_time[j,2],Y_predict[j],power_round,holiday]

        c.insert_powerprediction15(df_predict_power.loc[cnt])
        cnt = cnt + 1
        j = j + 1

    # 실제전력 및 예측전력
    real_power = df_predict_power["realpower"].to_numpy()
    predict_power = df_predict_power["predictpower"].to_numpy()

    """
    print("real_power:", real_power)
    print("predict_power:", predict_power)

    # 성능평가 지수
    cvmbe = (np.mean(predict_power - real_power)) / np.mean(real_power)
    wape = (mean_absolute_error(predict_power, real_power)) / np.mean(real_power)
    mape = np.mean(np.abs((real_power - predict_power) / real_power))
    cvrmse = (np.sqrt(mean_squared_error(predict_power, real_power))) / np.mean(real_power)

    print("\n   예측전력 합계  ", math.fsum(predict_power))
    print("")
    print('MBE      : ' + str(round(cvmbe * 100, 2)) + " %")
    print('MAE      : ' + str(round(wape * 100, 2)) + " %")
    print('Cv(RMSE) : ' + str(round(cvrmse * 100, 2)) + " %\n")
    """

    # 최적 알고리즘 및 초매개변수 출력
    for algo, params in zip(model_algo, model_params):
        df_algorithm.loc[n] = [algo]
        n = n + 1
        print(algo, " ", params)
    print("")

    """
    # 예측전력을 날짜별, 시간별, 분별로 그룹화
    df_predict_power.sort_values(["date", "hour", "min"], ascending=True, inplace=True)
    df_predict_min_power = df_predict_power.groupby(["date", "hour", "min"], as_index=False)
    df_predict_min_power = df_predict_min_power.agg({'realpower': 'sum', 'predictpower': 'sum'})
    df_predict_hour_power = df_predict_power.groupby(["date", "hour"], as_index=False)
    df_predict_hour_power = df_predict_hour_power.agg({'realpower': 'sum', 'predictpower': 'sum'})
    df_predict_date_power = df_predict_power.groupby(["date"], as_index=False)
    df_predict_date_power = df_predict_date_power.agg({'realpower': 'sum', 'predictpower': 'sum'})

    # 엑셀 여러 sheet에 저장
    writer = pd.ExcelWriter('./wonju-predict-power-min.xlsx', engine='xlsxwriter', datetime_format='yyyy-mm-dd')
    df_predict_min_power.to_excel(writer, sheet_name='분별', index=False)
    df_predict_hour_power.to_excel(writer, sheet_name='시간별', index=False)
    df_predict_date_power.to_excel(writer, sheet_name='날짜별', index=False)
    writer.save()
    """

    end = time.time()
    print("소요시간: ", end - start)

sitecode = ''
c = Common(sitecode)
sitecode = c.site_code()

# print("predictdate:", predictdate)
# op_date_list = c.op_days('20200206', '20210118')
# print("op_date_list:\n", op_date_list)
#PowerPrediction_15M(e_src, p_year, p_month, p_day, p_hour, p_min)

"""       
for predict_hour in range(int(float(workstarttime)//100), math.ceil(float(workendtime)/100)):
    print("predict_hour:", predict_hour)
    PowerPrediction_15M(predict_hour)
#df_date = c.op_days('20200305','20200311')
df_date = c.op_days('20200312','20210118')
for i in range(320):
    predictdate =  df_date.values[i][0]
    print("predictdate:", i, predictdate)
    predict_date = datetime.datetime.strptime(predictdate, '%Y%m%d')
    print("predict_date:", predict_date)
    start_date = predict_date - datetime.timedelta(days=past_day)
    predict_next_date = predict_date + datetime.timedelta(days=1)
    predictdate_nextday = predict_next_date.strftime("%Y%m%d")
    predictdate = predict_date.strftime("%Y%m%d")
    startdate = start_date.strftime("%Y%m%d")

    for predict_hour in range(int(float(workstarttime)//100), math.ceil(float(workendtime)/100)):
        print("predict_hour:", predict_hour)
        PowerPrediction_15M(predict_hour)
"""
