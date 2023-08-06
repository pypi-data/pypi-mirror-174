# power_predict_hourly.py
# 1시간 전력예측(주말 주초 및 기온민감도, 전력량 클러스터링 추가)

from common_function import Common
import pandas as pd
import numpy as np
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
from tslearn.clustering import KShape
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

p_year = 2022
p_month = 8
p_day = 2
p_hour = 15
energy_source =2

def PowerPrediction_hourly(energy_source, p_year, p_month, p_day, p_hour):

    # start = time.time()
    random_seed = 42
    cnt = 0
    n = 0

    model_algo = []
    model_params = []

    df_predict_power = pd.DataFrame(columns=['date', 'hour', 'realpower', 'predictpower', 'weekholiday'])
    df_algorithm = pd.DataFrame(columns=['algorithm'])

    # 예측일시
    past_day = 30
    predictdate = datetime.datetime(p_year, p_month, p_day)
    predict_time = datetime.time(p_hour)

    predict_hour = predict_time.hour
    startdate = predictdate - datetime.timedelta(days=past_day)
    predict_date = predictdate.strftime("%Y%m%d")

    start_date = startdate.strftime("%Y%m%d")
    predictdate_nextday = (predictdate + datetime.timedelta(days=1)).strftime("%Y%m%d")

    # 데이터 가져오기
    workstarttime, workendtime = c.wokr_time()
    df_all_power = c.select_power_real_15m(energy_source)
    df_all_real_weather = c.weather_real_info()
    df_all_predict_weather = c.weather_predict_info()

    df_all_power = reduce(df_all_power)
    # 기상실황 노점온도 및 습구온도 속성 추가
    df_dew_wet = c.calculation_dew_wet_temp(df_all_real_weather['Temp'].values, df_all_real_weather['Reh'].values)
    df_all_real_weather[['Dew_temp', 'Wet_temp']] = df_dew_wet[['Dew_temp', 'Wet_temp']]

    # 기상예측 노점온도 및 습구온도 속성 추가
    df_dew_wet = c.calculation_dew_wet_temp(df_all_predict_weather['Temp'].values, df_all_predict_weather['Reh'].values)
    df_all_predict_weather[['Dew_temp', 'Wet_temp']] = df_dew_wet[['Dew_temp', 'Wet_temp']]

    # 휴일 여부 데이터프레임 생성 시작
    # 과거일의 휴일여부
    df_holiday = pd.DataFrame(columns=['Date', 'WeekHoliday'])
    holiday_code = c.get_holiday_day()
    df_all_power = df_all_power.astype({'RealDate':'str'})

    df_all_before_power = df_all_power[(df_all_power['RealDate'] >= start_date) & (df_all_power['RealDate'] < predict_date)]
    df_holiday['Date'] = df_all_before_power['RealDate']
    df_holiday['WeekHoliday'] = df_all_before_power['WeekHoliday']
    df_holiday.drop_duplicates(['Date', 'WeekHoliday'], keep='first', inplace=True)
    df_holiday.reset_index(drop=True, inplace=True)
    holiday_cnt = len(df_holiday)
    # print("df_holiday", df_holiday)

    # 예측일의 휴일여부
    for p_cnt in range(3):
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
        # print("next_date", next_date, "isholiday", isholiday, holiday_code, next_date.weekday())

    # 휴일 여부 데이터프레임 생성 끝

    if predict_hour == 0:
        predictyesterday = predictdate - datetime.timedelta(days=1)
        predict_yesterday = predictyesterday.strftime("%Y%m%d")
        holiday = df_holiday.loc[df_holiday['Date'] == predict_yesterday]['WeekHoliday'].values[0]
    else:
        holiday = df_holiday.loc[df_holiday['Date'] == predict_date]['WeekHoliday'].values[0]

    # 미래 휴일 코드 추가  predictdate_nextday

    # 평일, 주말, 주초, 휴일 속성 추가
    df_holiday['Daytype'] = df_holiday['WeekHoliday']
    h_index = df_holiday.loc[df_holiday['WeekHoliday'] == 0].index.values  # 휴일 인덱스
    idx_cnt = len(h_index)

    if df_holiday.iloc[-1, 1] == 0:
        idx_cnt = idx_cnt - 1

    for index in range(idx_cnt):
        idx = h_index[index]
        if idx > 0 and df_holiday.iloc[idx - 1, 1] == 1:  # 일반 평일
            # print("df_holiday.iloc[", idx-1, "]", df_holiday.iloc[idx-1])
            df_holiday.iloc[idx - 1, 2] = 2  # 주말
        if df_holiday.iloc[idx + 1, 1] == 1:
            df_holiday.iloc[idx + 1, 2] = 3  # 주초
    df_holiday.sort_values(['Date'], ascending=True,inplace=True)
    df_holiday.reset_index(drop=True, inplace=True)
    #################################################

    # 일자 및 시간 속성 추가
    df_all_power['Savetime'] = pd.to_datetime(df_all_power['Savetime'])
    df_all_power['Savetime'] = df_all_power['Savetime'] + datetime.timedelta(minutes=45)
    df_all_power['Date'] = df_all_power['Savetime'].dt.strftime("%Y%m%d")
    df_all_power['Hour'] = df_all_power['Savetime'].dt.hour
    df_all_power['Min'] = df_all_power['Savetime'].dt.minute
    df_all_power['Count'] = 1
    df_all_power.drop(['Savetime', 'RealDate', 'RealHour', 'RealMin', 'WeekHoliday'], axis=1, inplace=True)

    # 1시간 간격 사용 전력량으로 15분 사용 전력량을 합함
    df_all_hour_power = df_all_power.groupby(["Date", "Hour"], as_index=True).agg({'RealPower15M': 'sum', 'Count': 'sum'})
    df_all_hour_power.reset_index(inplace=True)
    df_all_hour_power = df_all_hour_power[df_all_hour_power['Count'] == 4]
    del df_all_hour_power['Count']
    #df_all_hour_power['WeekHoliday'] = df_all_hour_power['WeekHoliday'].apply(lambda x: 1 if x==4 else x)
    #df_all_hour_power['WeekHoliday'] = df_all_hour_power['WeekHoliday'].apply(lambda x: 0 if x==3 else x)

    # 예측전력을 날짜별, 시간별, 분별로 그룹화
    df_all_hour_power.sort_values(["Date", "Hour"], ascending=True, inplace=True)
    df_all_date_power = df_all_hour_power.groupby(["Date"], as_index=False)
    df_all_date_power = df_all_date_power.agg({'RealPower15M': 'sum'})

    """
    # 엑셀 여러 sheet에 저장
    path = "./ibs-all-power.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter', datetime_format='yyyy-mm-dd')
    df_all_hour_power.to_excel(writer, sheet_name='시간별', index=False)
    df_all_date_power.to_excel(writer, sheet_name='날짜별', index=False)
    writer.save()
    """

    # 시간별 근무 여부 데이터프레임
    df_work_hour = pd.DataFrame(columns=['Hour', 'Work'])

    # 시간별 근무 여부 데이터프레임 (근무시간에는 1, 근무시간 외에는 0)
    for i in range(0, 24):
        if (i >= float(workstarttime)) & (i <= math.ceil(float(workendtime))):
            df_work_hour.loc[i] = [i, 1]
        else:
            df_work_hour.loc[i] = [i, 0]

    # DB 테이블에 입력된 시간 특성으로 일반 시간으로 맞추기 위함
    df_all_real_weather['Hour'] = pd.to_numeric(df_all_real_weather['Hour'])
    df_all_predict_weather['Hour'] = pd.to_numeric(df_all_predict_weather['Hour'])

    #pd.set_option('display.max_columns', None)

    start = time.time()

    # 시간별 전력 예측
    #for n_hour in range(predict_hour, predict_hour + 1):
        
    # 기상정보 클러스터링
    df_real_weather1 = df_all_real_weather[(df_all_real_weather['Date'] >= start_date) &
                                           (df_all_real_weather['Date'] < predict_date)]
    df_real_weather2 = df_all_real_weather[(df_all_real_weather['Date'] == predict_date) &
                                           (df_all_real_weather['Hour'] < predict_hour)]

    df_predict_weather = df_all_predict_weather[((df_all_predict_weather['Date'] == predict_date) &
                                                 (df_all_predict_weather['Hour'] >= predict_hour)) |
                                                ((df_all_predict_weather['Date'] == predictdate_nextday) &
                                                 (df_all_predict_weather['Hour'] < predict_hour))]

    df_weather = pd.concat([df_real_weather1, df_real_weather2, df_predict_weather])
    df_weather['Date'] = pd.to_datetime(df_weather['Date'])
    df_weather['Week'] = df_weather['Date'].dt.weekday     #  + 1
    df_weather['Month'] = df_weather['Date'].dt.month
    df_weather['Day'] = df_weather['Date'].dt.day
    df_weather['Date'] = df_weather['Date'].dt.strftime("%Y%m%d")

    pd.set_option('display.max_rows', None)
    #print("@@@ df_holiday:\n", df_holiday)
    #print("### df_weather:\n", df_weather)
    # holiday 속성 및 work 추가 및 정리
    #print("merge\n", pd.merge(df_weather, df_holiday, on=('Date')))
    df_weather = pd.merge(pd.merge(df_weather, df_holiday, on=('Date')), df_work_hour, on=('Hour'))
    df_weather.loc[df_weather['WeekHoliday'] == 0, 'Work'] = 0
    df_weather = df_weather.sort_values(by=['Date', 'Hour'])

    # ------------------ 기상정보 K-Means 클러스터링 시작 --------------------------------------
    X_cluster = df_weather[['Hour', 'WeekHoliday', 'Temp', 'Reh', 'Dew_temp', 'Wet_temp']].values
    df_cluster = c.climate_clustering(X_cluster)

    # 클러스터 값을 데이터프레임 cluster에 추가
    df_weather['Cluster'] = df_cluster.values
    # ------------------ 기상정보 K-Means 클러스터링 끝 ----------------------------------------

    # ------------------ 습구온도 Kshape 클러스터링 시작 --------------------------------
    df_predict_weather2 = df_all_predict_weather[
        (df_all_predict_weather['Date'] == predictdate_nextday) & (df_all_predict_weather['Hour'] >= predict_hour)]

    df_weather2 = pd.concat([df_weather, df_predict_weather2])
    df_weather2 = df_weather2.iloc[len(df_weather2) % 24:, :]

    df_date = df_weather2['Date'].unique()
    df_temp = df_weather2['Wet_temp']

    #print("len(df_date):", len(df_date))
    #print("df_date:", df_date)
    #print("df_temp:", df_temp)
    temp = df_temp.values.reshape((len(df_date), 24))
    temp_train = TimeSeriesScalerMeanVariance().fit_transform(temp)

    df_cluster = c.temp_clustering_1hour(df_date, temp_train)

    # 습구온도 클러스터 값 속성으로 추가
    df_weather = pd.merge(df_weather, df_cluster, on=('Date'))
    # ------------------ 습구온도 kshape 클러스터링 끝 --------------------------------------

    # 과거 전력 데이터 가져오기
    df_past_power = df_all_hour_power[((df_all_hour_power['Date'] >= start_date) &
                                       (df_all_hour_power['Date'] < predict_date)) |
                                      ((df_all_hour_power['Date'] == predict_date) &
                                       (df_all_hour_power['Hour'] < predict_hour))]  #

    df_past_power = df_past_power.sort_values(by=['Date', 'Hour'])
    # to_index = df_past_power[(df_past_power['Date'] == predictdate) & (df_past_power['Hour'] == n_hour)].index
    # df_past_power = df_past_power.loc[:to_index[0] - 1, :]

    # 과거 전력 데이터와 기상 데이터 병합
    df_past_power = pd.merge(df_past_power, df_weather, on=('Date', 'Hour'))
    #print("df_past_power\n", df_past_power.tail())

    # 기상 민감도 속성
    df_sense_power = df_past_power[['WeekHoliday', 'Hour', 'Temp', 'Reh', 'Dew_temp', 'Wet_temp', 'RealPower15M']]
    if (df_sense_power.groupby(["WeekHoliday", "Hour"]).size() > 1).all():
        df_sensitivity = c.sensitivity_generation_hourly(df_sense_power, predict_hour, holiday)

    # 이상치 제거
    outlier_index_all = np.array([])
    hour_list = df_past_power['Hour'].unique()

    for hour_no in hour_list:
        for holiday_no in range(2):
            df_hour = df_past_power[(df_past_power['Hour']==hour_no) & (df_past_power['WeekHoliday'] == holiday_no)]
            outlier_index = c.get_outlier(df=df_hour, column='RealPower15M', weight=1.5, min=60)
            if outlier_index.size > 0:
                outlier_index_all = np.append(outlier_index_all, outlier_index)
    df_past_power.drop(outlier_index_all, axis=0, inplace=True)

    # 이상치 제거 후
    df_real = df_past_power.sort_values(by=['Date', 'Hour'])
    df_real_target = df_real['RealPower15M']
    df_real = df_real.drop(['RealPower15M'], axis=1)
    #df_real.reset_index(drop=True, inplace=True)

    # 미래 데이터 생성
    df_predict = df_weather.iloc[-len(df_predict_weather):, :]
    df_predict.reset_index(drop=True, inplace=True)

    """
    p_index = df_predict.loc[df_predict['Hour'] == 0].index.values[0]  # 0시 인덱스
    df_predict.iloc[p_index, 6:11] = df_predict.iloc[p_index - 1, 6:11]  # 어제 휴일 등 코드
    df_predict = df_predict.iloc[1:]
    """
    # print("df_predict:\n",df_predict)

    # 평일 휴일별 시간별 전력 통계량(최소, 최대, 평균)
    df_past_power_stat = df_past_power.groupby(['WeekHoliday','Hour']).agg({'RealPower15M':['min', 'max', 'mean']})
    df_past_power_stat.reset_index(inplace=True)

    # 전력량 통계량 속성 추가
    df_real = pd.merge(df_real, df_past_power_stat, on=('WeekHoliday', 'Hour'))
    df_predict = pd.merge(df_predict, df_past_power_stat, on=('WeekHoliday', 'Hour'))

    """
    # 성능 측정용 미래 전력 데이터 (테스트시 사용, 실제는 없는 데이터)
    Y_predict = df_all_hour_power[((df_all_hour_power['Date'] == predict_date) &
                                   (df_all_hour_power['Hour'] >= predict_hour)) |
                                  ((df_all_hour_power['Date'] == predictdate_nextday) &
                                   (df_all_hour_power['Hour'] < predict_hour))]['RealPower15M'].values
    """

    #print("predict_date", predict_date, "predict_hour", predict_hour, "predictdate_nextday", predictdate_nextday)
    # 과거 데이터와 미래 데이터 통합
    df_total = pd.concat([df_real, df_predict])

    # 기상 민감도 속성 추가
    if len(df_sensitivity) > 0:
        df_total = pd.merge(df_total, df_sensitivity, on=('WeekHoliday', 'Hour'))
        df_total.sort_values(["Date", "Hour"], ascending=True, inplace=True)

    # 원핫인코딩
    df_dummy = pd.get_dummies(df_total, columns=['Hour', 'Week', 'Daytype', 'Cluster', 'Work', 'Temp_cluster'])
    df_dummy[['Hour']] = df_total[['Hour']]

    df_real_dummy = df_dummy.iloc[:-len(df_predict), :]
    df_predict_dummy = df_dummy.iloc[-len(df_predict):, :]

    # 입력 데이터와 목표 데이터 분리
    df_real_input = df_real_dummy.drop(['Date', 'Day', 'Month', 'Hour'], axis=1)
    df_real_input['Hour'] = df_real_dummy['Hour']

    df_predict_time = df_predict_dummy[['Date', 'Hour', 'WeekHoliday']]

    df_predict_input = df_predict_dummy.drop(['Date', 'Day', 'Month', 'Hour'], axis=1)

    X = df_real_input.values
    Y = df_real_target.values
    X_predict = df_predict_input.values

    """
    # 가비지 컬렉션
    del df_past_power, df_sense_power, df_real, df_predict, df_total, df_cluster,\
        df_real_weather1, df_real_weather2, df_predict_weather, df_weather, df_sensitivity, \
        df_real_input, df_predict_input, df_dew_wet, df_dummy, df_real_dummy, df_predict_dummy, X_cluster
    gc.collect()
    """

    # 학습 데이터와 시험 데이터 분리
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, stratify=X[:, -1],
                                                        random_state=random_seed)

    # 훈련 데이터 n배 더 추가
    for p in range(1):
        xTrainTemp, xTestTemp, yTrainTemp, yTestTemp = \
            train_test_split(X, Y, test_size=0.3, stratify=X[:, -1], random_state=random_seed)
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
    for i in range(len(df_predict_time['Hour'])):
        if len(str(df_predict_time.iloc[i, 1])) == 1:
            df_predict_time.iloc[i, 1] = "0" + str(df_predict_time.iloc[i, 1]) + "00"
        elif len(str(df_predict_time.iloc[i, 1])) == 2:
            df_predict_time.iloc[i, 1] = str(df_predict_time.iloc[i, 1]) + "00"

    X_time = df_predict_time.values

    # 최적화 결과 mse가 작은 순으로 정렬 및 알고리즘, 초매개변수 저장
    output.sort_values(["mse"], ascending=True, inplace=True)
    model_algo = np.append(model_algo, output.iloc[0, 0])
    model_params = np.append(model_params, output.iloc[0, 3])


    #print("X_time\n", X_time)
    #print("df_predict_time['Hour']:", df_predict_time['Hour'])
    #print("df_predict_time.values:", df_predict_time.values)

    #print("output.iloc[0, 2]", output.iloc[0, 2])
    # 실제전력 및 예측전력 출력
    j = 0
    for i in output.iloc[0, 2]:
        #print("j:", j, "i", i)
        i = np.float64(i*0.8 + output.iloc[1,2][j]*0.2)
        #i = np.float64(i)
        #i = output.iloc[0, 2][i]
        power_round = np.around(i)

        # 예측전력이 0보다 적은 경우 예측전력 0
        if power_round < 0:
            power_round = 0

        # 첫 시간은 15분 전력에서 예측한 전력량으로 맞춘다
        # 테스트 후 실제 15분 생성 데이터 있으면 코멘트 풀 것!!!
        """
        """
        if j == 0:
            sdate = datetime.datetime(int(X_time[0, 0][0:4]), int(X_time[0, 0][4:6]), int(X_time[0, 0][6:8]), int(X_time[0, 1][0:2]), 0)
            edate = sdate + datetime.timedelta(minutes=60)

            s_date = sdate.strftime("%Y%m%d%H%M")
            e_date = edate.strftime("%Y%m%d%H%M")
            sum_predictpower15m = c.sum_predictpower15m_hourly(energy_source, s_date, e_date)
            power_round = np.around(sum_predictpower15m)
            # print("1시간 예측치:", power_round)

        print("일자 %s " % (X_time[j, 0]), "시간 %s " % (X_time[j, 1]), "예측전력 %.2f " % power_round,
              "휴일여부 %d " % (X_time[j, 2]), "알고리즘 %s " % output.iloc[0, 0])

        df_predict_power.loc[cnt] = [X_time[j, 0], X_time[j, 1], 0, power_round, X_time[j, 2]]
        c.insert_powerprediction_hourly(df_predict_power.loc[cnt])
        cnt = cnt + 1
        j = j + 1

    # 실제전력 및 예측전력
    real_power = df_predict_power["realpower"].to_numpy()
    predict_power = df_predict_power["predictpower"].to_numpy()

    # 정규화된 지니계수
    def eval_gini(y_real, y_pred):
        assert y_real.shape == y_pred.shape  # 실제값과 예측값의 크기가 서로 같은지 확인

        n_samples = y_real.shape[0]  # 데이터 개수
        L_mid = np.linspace(1 / n_samples, 1, n_samples)  # 대각선 값

        # 예측값에 대한 지니계수
        pred_order = y_real[y_pred.argsort()]  # y_pred 크기 순으로 y_real 값 정렬
        L_pred = np.cumsum(pred_order) / np.sum(pred_order)  # 로렌츠 곡선
        G_pred = np.sum(L_mid - L_pred)  # 예측값에 대한 지니계수

        # 실제값에 대한 지니계수(예측이 완벽할 때 지니계수)
        real_order = y_real[y_real.argsort()]  # y_real 크기 순으로 y_real 값 정렬
        L_real = np.cumsum(real_order) / np.sum(real_order)  # 로렌츠 곡선
        G_real = np.sum(L_mid - L_real)  # 예측이 완벽할 때 지니계수

        return G_pred / G_real

    """
    # 성능평가 지수
    cvmbe = (np.mean(predict_power - real_power)) / np.mean(real_power)
    wape = (mean_absolute_error(predict_power, real_power)) / np.mean(real_power)
    mape = np.mean(np.abs((real_power - predict_power) / real_power))
    cvrmse = (np.sqrt(mean_squared_error(predict_power, real_power))) / np.mean(real_power)
    gini_coeff = eval_gini(real_power, predict_power)

    print("\n   예측전력 합계  ", math.fsum(predict_power))
    print('\nCv(MBE) : ' + str(round(cvmbe * 100, 2)) + " %")
    print('WAPE     : ' + str(round(wape * 100, 2)) + " %")
    print('MAPE     : ' + str(round(mape * 100, 2)) + " %")
    print('Cv(RMSE) : ' + str(round(cvrmse * 100, 2)) + " %")
    print('예측율    : ' + str(round(100 - mape * 100, 2)) + " %")
    print('정규화된 지니계수 : ' + str(round(gini_coeff * 100, 2)) + " %\n")
    """

    # 최적 알고리즘 및 초매개변수 출력
    for algo, params in zip(model_algo, model_params):
        df_algorithm.loc[n] = [algo]
        n = n + 1
        print(algo, " ", params, "\n")
    #print("")

    # 예측전력을 날짜별, 시간별, 분별로 그룹화
    df_predict_power.sort_values(["date", "hour"], ascending=True, inplace=True)
    df_predict_date_power = df_predict_power.groupby(["date"], as_index=False)
    df_predict_date_power = df_predict_date_power.agg({'realpower': 'sum', 'predictpower': 'sum'})

    # 엑셀 여러 sheet에 저장
    path = "./wonju-predict-power-" + predictdate.strftime("%Y%%d") + ".xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter', datetime_format='yyyy-mm-dd')
    df_predict_power.to_excel(writer, sheet_name='시간별', index=False)
    df_predict_date_power.to_excel(writer, sheet_name='날짜별', index=False)
    writer.save()

    end = time.time()
    print("소요시간: ", end - start)

sitecode = ''
c = Common(sitecode)
sitecode = c.site_code()

# PowerPrediction_hourly(energy_source, p_year, p_month, p_day, p_hour)

"""
df_date = c.op_days('20200428','20210118')
for i in range(270):
    predictdate =  df_date.values[i][0]
    print("predictdate:", i, predictdate)
    predict_date = datetime.datetime.strptime(predictdate, '%Y%m%d')
    print("predict_date:", predict_date)
    start_date = predict_date - datetime.timedelta(days=past_day)
    predict_next_date = predict_date + datetime.timedelta(days=1)
    predictdate_nextday = predict_next_date.strftime("%Y%m%d")
    predictdate = predict_date.strftime("%Y%m%d")
    startdate = start_date.strftime("%Y%m%d")
    PowerPrediction_hourly(predict_hour)
"""
