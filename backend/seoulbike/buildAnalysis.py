from . import cron
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from korean_lunar_calendar import KoreanLunarCalendar
from .models import Bikespot, BikeHistory
import joblib

class weatherForecast:
    def __init__(self) -> None:
        tmpDict = cron.getWeatherForecast()
        self.weather = self.interpreter(tmpDict)

    def interpreter(self, tmpWeather):
        forecast = {}
        try:
            for timehour ,weatherDict in tmpWeather.items():
                tmpDict = {}
                tmpDict['비 또는 눈'] = 0
                if weatherDict['SNO']=='적설없음':
                    snow = 0.0
                elif '~' in weatherDict['SNO']:
                    x, y = weatherDict['SNO'].split('~')
                    snow = (float(x) + float(y[:-2]))/2
                else:
                    snow = float(weatherDict['SNO'][:-2])
                    tmpDict['비 또는 눈'] = 1
                if weatherDict['PCP']=='강수없음':
                    rain = 0.0
                elif '~' in weatherDict['PCP']:
                    x, y = weatherDict['PCP'].split('~')
                    rain = (float(x) + float(y[:-2]))/2
                else:
                    rain = float(weatherDict['PCP'][:-2])
                    tmpDict['비 또는 눈'] = 1
                tmpDict['강수량(mm)'] = rain + snow*10.0
                tmpDict['기온'] = float(weatherDict['TMP'])
                tmpDict['습도'] = float(weatherDict['REH'])
                tmpDict['불쾌지수'] = 1.8*tmpDict['기온'] - 0.558*(1-tmpDict['습도']/100)+(1.8*tmpDict['기온']-26)+32
                forecast[timehour] = tmpDict
        except:
            pass  #완성되지 않는 dictionary 제거

        return forecast

    def cronjob(self):
        tmpDict = cron.getWeatherForecast()
        self.weather = self.interpreter(tmpDict)


class Forecast:
    def __init__(self):  #최초 분석시에 실행
        now = datetime.now() 
        for i in range(217):
            eachtime = now-timedelta(hours=216-i)
            timestring = str(eachtime.year)+str(eachtime.month).zfill(2)+str(eachtime.day).zfill(2)+str(eachtime.hour).zfill(2)
            print(timestring)
            cron.putHistoryDB(timestring)
        self.timestring = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)
        self.forecast = weatherForecast()
        self.LunarCalender = KoreanLunarCalendar()
        self.liftHolidays = ['0101', '0301', '0505', '0606', '0815', '1003', '1009', '1225']
        self.lunarHolidays = ['1230', '0101', '0102', '0408', '0814', '0815', '0816']
        self.sunrise = {1:7.5, 2:7, 3:6.5, 4:5.5, 5:5, 6:5, 7:5, 8:5, 9:5.5,10:6.0, 11: 6.5, 12:7}
        self.sunset = {1:18, 2:18.5, 3:19, 4:19.5, 5:20, 6:20.5, 7:20, 8:20, 9:19,10:18.5, 11: 18, 12:17.5}
        self.timeindex = None
        self.dataframe = self.makeGeneralColumns(now)
        self.infodf = self.dataframe.loc[:,['기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수']].copy()  #'기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수' 알림의 대상이 되는 정보들 리턴
        self.infodf.columns = ['temp', 'rainfall', 'snowrain', 'holiday', 'uncomf']

        self.results = {}

    def timeCheck(self):  #분석 시도할때마다 체크 
        now = datetime.now() 
        nowstring = str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2)+str(now.hour).zfill(2)
        print(cron.historyUpdated)
        if nowstring !=self.timestring and cron.historyUpdated==True:  #만약 시간이 새로 바뀌어 업데이트해야한다면
            if(now.hour%3==0):
                self.forecast.cronjob()   #3시간 간격으로는 forecast를 받아옴

            self.dataframe = self.makeGeneralColumns(now)  #데이터프레임을 새로만들고
            self.infodf = self.dataframe.loc[:,['기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수']].copy()  #'기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수' 알림의 대상이 되는 정보들 리턴
            self.infodf.columns = ['temp', 'rainfall', 'snowrain', 'holiday', 'uncomf']
            self.results = {} #이미 제공된 분석들을 초기화
            self.timestring = nowstring
            cron.historyUpdated=False
        
    def getForecast(self, idnumber):        #분석을 가져가는 메소드
        self.timeCheck()            
        if idnumber in self.results:        #이미 만들어진 결과가 있으면 그것을 리턴
            return {**self.results[idnumber], "info" : self.infodf }
        histdf, completedf = self.makeSpecificColumns(idnumber) #없으면 데이터프레임부터 완성
        sign, borrow_model, return_model, mms = self.getModel(idnumber)
        returnDict = {}
        if not sign:        #모델이 없으면 history만 제공
            returnDict = {"result" : False, "history" : histdf}
            self.results.update({idnumber : returnDict})
            return returnDict
        mmsdf = mms.transform(completedf)           #모델로 predict
        borrow_pred = borrow_model.predict(mmsdf)
        return_pred = return_model.predict(mmsdf)
        returnDict = {"result" : True, "borrow" : borrow_pred, "return" : return_pred, "index" : self.timeindex, "history" : histdf }
        self.results.update({idnumber : returnDict})
        return {**returnDict, "info" : self.infodf }

    def getModel(self, idnumber):       #모델을 파일로부터 불러옴
        idstr = str(idnumber)
        try:
            borrow_model = joblib.load('static/analysis/models/seoulbike_{0}_대여.pkl'.format(idstr))
            return_model = joblib.load('static/analysis/models/seoulbike_{0}_반납.pkl'.format(idstr))
            mms = joblib.load('static/analysis/scalers/seoulbike_mms_{0}.pkl'.format(idstr))
        except Exception as e:
            return False, None, None, None
        return True, borrow_model, return_model, mms

    def makeSpecificColumns(self, idnumber):        #대여소마다 바뀌는 칼럼들을 만듦
        completedf = self.dataframe.copy()
        bikespot = Bikespot.objects.get(idnumber=idnumber)
        completedf['경과도'] = np.sqrt(1+pd.to_timedelta(completedf.index.date - bikespot.open_date).days)
        histdf = self.historydf(idnumber)
        completedf['유출량(-49)'] = list(histdf.iloc[217-49:217-49+48, 3])
        completedf['유출량(-72)'] = list(histdf.iloc[217-72:217-72+48, 3])
        completedf['유출량(-73)'] = list(histdf.iloc[217-73:217-73+48, 3])
        completedf['유출량(-96)'] = list(histdf.iloc[217-96:217-96+48, 3])
        completedf['유출량(-97)'] = list(histdf.iloc[217-97:217-97+48, 3])
        completedf['유출량(-120)'] = list(histdf.iloc[217-120:217-120+48, 3])
        completedf['유출량(-121)'] = list(histdf.iloc[217-121:217-121+48, 3])
        completedf['유출량(-144)'] = list(histdf.iloc[217-144:217-144+48, 3])
        completedf['유출량(-145)'] = list(histdf.iloc[217-145:217-145+48, 3])
        completedf['유출량(-168)'] = list(histdf.iloc[217-168:217-168+48, 3])
        completedf['유출량(-169)'] = list(histdf.iloc[217-169:217-169+48, 3])
        completedf['유출량(-192)'] = list(histdf.iloc[217-192:217-192+48, 3])
        completedf['유출량(-193)'] = list(histdf.iloc[217-193:217-193+48, 3])
        completedf['유출량(-216)'] = list(histdf.iloc[217-216:217-216+48, 3])
        return histdf, completedf
      
    def historydf(self, idnumber): #DB에서 유출량 뽑아내기
        start = self.dataframe.index[0]-timedelta(days=9, hours=1)  #유출량을 계산하려면 한 줄 더필요함
        startInt = start.year*10000+start.month*100+start.day
        history = BikeHistory.objects.filter(spot=idnumber, date__gte=startInt).order_by('date', 'hour')
        df = pd.DataFrame.from_records(history.values())
        df = pd.concat([df, df.loc[:,'have'].shift(-1)], axis=1)
        df['outflow'] = df.iloc[:,4] - df.iloc[:,5]
        df.columns = ['id', 'date', 'hour', 'spot', 'have', 'have-1', 'outflow']
        df.drop(['id','spot','have-1'],axis = 1, inplace=True)
        df.fillna(0, inplace=True)
        return df

    def makeGeneralColumns(self, now):  #시간마다 업데이트, 모든 대여소에서 쓰이는 칼럼들을 빌드
        now = now.replace(minute=0, second=0, microsecond=0)
        newindex = pd.date_range(now, periods=48, freq="H")
        self.timeindex = newindex
        newdf = pd.DataFrame(columns=['시', '월', '기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수',
        '경과도', '2020년', '광도', '출근', '퇴근', '유출량(-49)', '유출량(-72)', '유출량(-73)', '유출량(-96)', '유출량(-97)',
       '유출량(-120)', '유출량(-121)', '유출량(-144)', '유출량(-145)', '유출량(-168)',
       '유출량(-169)', '유출량(-192)', '유출량(-193)', '유출량(-216)'] , index=newindex)
        
        newdf['시'] = newdf.index.hour
        newdf['월'] = newdf.index.month
        newdf['2020년'] = 0
        newdf['휴일'] = pd.to_datetime(newindex).map(self.isHoliday)
        newdf['출근'] = (1-newdf['휴일'])*((newdf['시'].isin([7,8,9])).astype(int) + (newdf['시'].isin([8])).astype(int)*2)
        newdf['퇴근'] = (1-newdf['휴일'])*((newdf['시'].isin([17,18,19])).astype(int) + (newdf['시'].isin([18])).astype(int)*2)
        newdf['광도'] = ((newdf['시'] - newdf['월'].replace(self.sunrise)>-1) & (newdf['월'].replace(self.sunset) - \
            newdf['시'] >0.5)).astype(int) + ((newdf['시'] - newdf['월'].replace(self.sunrise)>0) & \
                (newdf['월'].replace(self.sunset) - newdf['시'] >0)).astype(int)
        indexMapper = newdf.index.strftime('%Y%m%d%H')
        print(indexMapper)
        print(self.forecast.weather)
        newdf["기온"] = indexMapper.map(lambda x: self.forecast.weather.get(x)['기온'])
        newdf["강수량(mm)"] = indexMapper.map(lambda x: self.forecast.weather.get(x)['강수량(mm)'])
        newdf["비 또는 눈"] = indexMapper.map(lambda x: self.forecast.weather.get(x)['비 또는 눈'])
        newdf["불쾌지수"] = indexMapper.map(lambda x: self.forecast.weather.get(x)['불쾌지수'])
        monthmin = newdf['월'].min()
        monthmax = newdf['월'].max()
        for i in range(1,monthmin):
            newdf['월_'+str(i)] = 0
        newdf = pd.get_dummies(newdf, columns=['월'])
        for i in range(monthmax+1, 13):
            newdf['월_'+str(i)] = 0
        newdf = pd.get_dummies(newdf, columns=['시'])

        return newdf

    def isHoliday(self, timeObj):
        if timeObj.dayofweek > 4:
            return 1
        monthdate = str(timeObj.month).zfill(2)+str(timeObj.day).zfill(2)
        if monthdate in self.liftHolidays:
            return 1
        self.LunarCalender.setSolarDate(timeObj.year, timeObj.month, timeObj.day)
        lunarmonthdate = self.LunarCalender.LunarIsoFormat().replace('-','')[4:]
        if lunarmonthdate in self.lunarHolidays:
            return 1
        return 0




