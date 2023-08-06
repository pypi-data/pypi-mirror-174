# main_power.py 전력예측 실행 프로그램
# cron 등록시 6분 21분 36분 51분에 실행되도록 함

# from common_function import Common
import make_power
from make_power import *
from power_predict_15m import *
from power_predict_hourly import *
import threading
import datetime as dt
from time import sleep
import sys

c = Common('')
sitecode = c.site_code()
print(sitecode, Common.sitecode)

# 실제로는 현재 날짜를 체크하여 실행
dt_now = dt.datetime.now()
p_year = dt_now.year
p_month = dt_now.month
p_day = dt_now.day
p_hour = dt_now.hour
p_min = dt_now.minute
print("현재시간 \np_year:", p_year, "p_month:", p_month, "p_day:", p_day, "p_hour:", p_hour, "p_min:", p_min)

prediction_time = dt.datetime(p_year, p_month, p_day, p_hour, p_min)
print("prediction_time:", prediction_time)
current_time = dt_now
print("current_time:", current_time)

# 테스트를 위해 테이블에 들어있는 데이터의 시간을 사용
current_time = dt.datetime(2022, 8, 2, 10, 27)
print("current_time:", current_time)
# make_power_15m(currenttime)
# c.execute_power_15m(currenttime)

c_year = current_time.year
c_month = current_time.month
c_day = current_time.day
c_hour = current_time.hour
c_min = current_time.minute

if len(sys.argv) >= 6:
    c_year = int(sys.argv[1])
    c_month = int(sys.argv[2])
    c_day = int(sys.argv[3])
    c_hour = int(sys.argv[4])
    c_min = int(sys.argv[5])

if 6 <= c_min < 21:
    c_min = 0
elif 21 <= c_min < 36:
    c_min = 15
elif 36 <= c_min < 51:
    c_min = 30
elif 51 <= c_min <= 59:
    c_min = 45
elif 0 <= c_min < 6:
    c_min = 45
    c_hour = c_hour - 1

print("실행시간 :", c_year, " 년", c_month, " 월", c_day, " 일", c_hour, " 시", c_min, " 분")

current_time = dt.datetime(c_year, c_month, c_day, c_hour, c_min)
predict_time = current_time + dt.timedelta(minutes=15)

p_year = predict_time.year
p_month = predict_time.month
p_day = predict_time.day
p_hour = predict_time.hour
p_min = predict_time.minute


print("예측시간 :", p_year, " 년", p_month, " 월", p_day, " 일", p_hour, " 시", p_min, " 분")

i = 0
while True:
    # 15분 데이터 생성을 실행하는 함수
    b15_make_time = current_time - dt.timedelta(minutes=15)
    print(" 15분 전력량 생성 : ", current_time)
    make_power.make_power_15m(current_time)
    #update_predict_power(b15_make_time.strftime("%Y%m%d%H%M"))
    #threading.Timer(90, make_power.make_power_15m(current_time)).start()

    energy_source = c.select_energy_src()
    # 15분 전력량 예측
    for e_src in energy_source:
        b_time = current_time - dt.timedelta(minutes=45)
        before_time = b_time.strftime("%Y%m%d%H%M")
        curr_time = current_time.strftime("%Y%m%d%H%M")
        # print("before_time", before_time, "curr_time", curr_time)

        cnt_15m, sum_realpower15m = c.count_power_real_15m(e_src, before_time, curr_time)
        # print("cnt_15m", cnt_15m, "sum_realpower15m", sum_realpower15m)
        #cnt_15m = c.count_power_real_15m(e_src, str(p_year), str(p_month).zfill(2), str(p_day).zfill(2), str(p_hour).zfill(4))
        if cnt_15m < 4 or sum_realpower15m <= 0:
            continue
        else :
            PowerPrediction_15M(e_src, p_year, p_month, p_day, p_hour, p_min)
            real_15power = c.select_real_15power(str(e_src), curr_time)
            c.update_predict_real15mpower(str(e_src), curr_time[0:8], curr_time[8:10]+'00', curr_time[10:12], real_15power)
        if p_min == 0:
            # 1시간 전력량 예측
            PowerPrediction_hourly(e_src, p_year, p_month, p_day, p_hour)

        #########
        if c_min == 0:
            # print("line 100   c_min:",c_min)
            sdate = current_time - datetime.timedelta(minutes=45)
            s_date = sdate.strftime("%Y%m%d%H00%M")
            e_date = current_time.strftime("%Y%m%d%H00%M")
            real_1hour_power = c.sum_real_1hour_power(str(e_src), s_date, e_date)
            c.update_predict_real1hourpower(str(e_src), curr_time[0:8], curr_time[8:10]+'00', real_1hour_power)
            # print("update_predict_real1hourpower 실행")

    current_time = current_time + datetime.timedelta(minutes=15)
    c_year = current_time.year
    c_month = current_time.month
    c_day = current_time.day
    c_hour = current_time.hour
    c_min = current_time.minute
    # print(current_time, dt.datetime.now())

    predict_time = current_time + dt.timedelta(minutes=15)
    p_year = predict_time.year
    p_month = predict_time.month
    p_day = predict_time.day
    p_hour = predict_time.hour
    p_min = predict_time.minute

    if i > 4:
        break
    i = i + 1
    # 15분 후에 전력 예측
    #time.sleep(900)


"""
# 주기 설정
job1= schedule.every(1).minutes.do(make_power_15m, currenttime + datetime.timedelta(minutes=15))

count = 0 
while True:
    schedule.run_pending()
    time.sleep(1)
    currenttime = currenttime + datetime.timedelta(minutes=15)
    count = count + 1

    if count > 2:
        schedule.cancel_job(job1)
"""
