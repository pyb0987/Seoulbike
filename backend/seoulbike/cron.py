from rest_framework import exceptions
import urllib.request
import time
import logging
import json
import sys
from django.db import transaction, IntegrityError
from . import models
from env_setting import *
from datetime import datetime, timedelta
from config.modelAPI import *

weather_table = {}
logger = logging.getLogger('cron')

this = sys.modules[__name__]
this.historyUpdated = False

def getBikeNum():  #매 5분마다 실행 / 매 1시간마다 코드 뒷쪽의 'db저장'부분이 실행됨

    
    url = "http://openapi.seoul.go.kr:8088/{0}/json/bikeList/{1}/{2}/"
    resultDict = {}
    for i in range(0, 3000, 1000):
        trynum = 3
        while trynum > 0:
            try:
                requrl = url.format(API_KEY_seoulbike, i+1, i+1000)
                request = urllib.request.Request(requrl)
                response = urllib.request.urlopen(request)
            except:
                logger.warning('api 호출 에러로 다시 시도. 남은 시도 : '+trynum)
                trynum -= 1
                if trynum == 0:
                    raise exceptions.PermissionDenied('api에 접근할 수 없습니다.', code=403)
                continue
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                responseDict = json.loads(response_body.decode('utf-8'))
                code = responseDict['rentBikeStatus']['RESULT']['CODE']
                if (code in ['INFO-100', 'ERROR-301', 'ERROR-310', 'INFO-200']):
                    logger.error('fetal error : url과 인증키, 또는 서비스 확인 요망. url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("url과 인증키, 또는 서비스 확인 요망", code=500)
                if (code in ['ERROR-300','ERROR-331', 'ERROR-332', 'ERROR-333', 'ERROR-334', 'ERROR-335', 'ERROR-336']):
                    logger.error('error : 잘못된 url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("error : 잘못된 url", code=500)
                if (code in ['ERROR-500', 'ERROR-600', 'ERROR-601']):
                    trynum -= 1
                    if trynum == 0:
                        raise exceptions.APIException("error : 따릉이 대여소의 정보를 확인할 수 없습니다.", code=400)    
                    time.sleep(10)
                    logger.warning('api측 오류로 다시 시도. 이후 남은 시도 : '+trynum)
                    continue
                for spot in responseDict['rentBikeStatus']["row"]:
                    try:
                        num, _ = spot['stationName'].split('.', 1)
                        resultDict[int(num)] = int(spot['parkingBikeTotCnt'])
                    except:
                        continue
                trynum = 0
            else:
                trynum -= 1
                if trynum == 0:
                    raise exceptions.APIException('api에서 원하는 정보를 얻을 수 없습니다.', code=404)
                logger.warning('api 연결 에러로 다시 시도. 이후 남은 시도 : '+trynum)
                time.sleep(10)

    try:
        with transaction.atomic():        

            bikespots = models.Bikespot.objects.all()[:]

            for bikespot in bikespots:
                bikenumber = resultDict.get(bikespot.idnumber)
                if isinstance(bikenumber, int):
                    bikespot.bike_number = resultDict.get(bikespot.idnumber)
                    bikespot.opened = True     #api 상황에 따라 특정 대여소들이 나왔다가 안나왔다가 함

                else:
                    bikespot.opened = False
                    bikespot.bike_number = 0
            models.Bikespot.objects.bulk_update(bikespots, ['bike_number','opened']) 
            this.historyUpdated = True
    except IntegrityError as e:
        logger.error('cronjob bulk_update 트랜젝션 에러')


    now = datetime.now()  
    updateTime = now-timedelta(hours=1)
    updateDate = int(str(updateTime.year)+str(updateTime.month).zfill(2)+str(updateTime.day).zfill(2))
    updateHour = int(str(updateTime.hour).zfill(2))
    if models.BikeHistory.objects.filter(date=updateDate, hour=updateHour).exists():    #1시간마다 DB에 히스토리 추가(이미 정보가 있으면 그냥 리턴해버림)
        return
    try:
        logger.error('cronjob db history 저장{0}'.format(updateDate+updateHour))   
        with transaction.atomic():        
            
            newHistories = [models.BikeHistory(date=updateDate, hour=updateHour, spot=idnumber, have=resultDict[idnumber] ) for idnumber in resultDict.keys() ]
            models.BikeHistory.objects.bulk_create(newHistories) 

    except IntegrityError as e:
        logger.error('cronjob 트랜젝션 에러')    

    if updateHour!=3:  #매일 오전 1시에 bikespot 업데이트
        return

    deleteTime = now-timedelta(days=10)
    deleteDate = int(str(deleteTime.year)+str(deleteTime.month).zfill(2)+str(deleteTime.day).zfill(2))
    if models.BikeHistory.objects.filter(date=deleteDate).exists():     #24시간마다 10일전 정보 제거하여 경량화(1시간마다 확인)
        queryset = models.BikeHistory.objects.filter(date=deleteDate)
        queryset.delete()


def updateSpots():  #매 1주일마다 실행

    url = "http://openapi.seoul.go.kr:8088/{0}/json/bikeList/{1}/{2}/"
    resultDict = {}
    for i in range(0, 3000, 1000):
        trynum = 3
        while trynum > 0:
            try:
                requrl = url.format(API_KEY_seoulbike, i+1, i+1000)
                request = urllib.request.Request(requrl)
                response = urllib.request.urlopen(request)
            except:
                logger.warning('api 호출 에러로 다시 시도. 남은 시도 : '+trynum)
                trynum -= 1
                if trynum == 0:
                    raise exceptions.PermissionDenied('api에 접근할 수 없습니다.', code=403)
                continue
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                responseDict = json.loads(response_body.decode('utf-8'))
                code = responseDict['rentBikeStatus']['RESULT']['CODE']
                if (code in ['INFO-100', 'ERROR-301', 'ERROR-310', 'INFO-200']):
                    logger.error('fetal error : url과 인증키, 또는 서비스 확인 요망. url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("url과 인증키, 또는 서비스 확인 요망", code=500)
                if (code in ['ERROR-300','ERROR-331', 'ERROR-332', 'ERROR-333', 'ERROR-334', 'ERROR-335', 'ERROR-336']):
                    logger.error('error : 잘못된 url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("error : 잘못된 url", code=500)
                if (code in ['ERROR-500', 'ERROR-600', 'ERROR-601']):
                    trynum -= 1
                    if trynum == 0:
                        raise exceptions.APIException("error : 따릉이 대여소의 정보를 확인할 수 없습니다.", code=400)    
                    time.sleep(10)
                    logger.warning('api측 오류로 다시 시도. 이후 남은 시도 : '+trynum)
                    continue
                for spot in responseDict['rentBikeStatus']["row"]:
                    try:
                        num, spotname = spot['stationName'].split('.', 1)
                        rackTotCnt = spot['rackTotCnt']
                        stationLatitude = spot['stationLatitude']
                        stationLongitude = spot['stationLongitude']
                        parkingBikeTotCnt = spot['parkingBikeTotCnt']
                        resultDict[int(num)] = {
                            'num' : num,
                            'spotname' : spotname,
                            'rackTotCnt' : rackTotCnt,
                            'stationLatitude' : stationLatitude,
                            'stationLongitude' : stationLongitude,
                            'parkingBikeTotCnt' : parkingBikeTotCnt
                        }
                    except:
                        continue
                trynum = 0
            else:
                trynum -= 1
                if trynum == 0:
                    raise exceptions.APIException('api에서 원하는 정보를 얻을 수 없습니다.', code=404)
                logger.warning('api 연결 에러로 다시 시도. 이후 남은 시도 : '+trynum)
                time.sleep(10)

    try:
        with transaction.atomic():        
            bikespots = models.Bikespot.objects.all()[:]
            for bikespot in bikespots:
                bikeDict = resultDict.get(bikespot.idnumber)
                if isinstance(bikeDict, dict):
                    bikespot.opened = True
                    bikespot.bike_number = int(bikeDict['parkingBikeTotCnt'])
                    bikespot.capacity = int(bikeDict['rackTotCnt'])
                    del resultDict[bikespot.idnumber]
                else:
                    bikespot.opened = False
                    bikespot.bike_number = 0
            models.Bikespot.objects.bulk_update(bikespots, ['bike_number','capacity','opened']) 
    except IntegrityError as e:
        logger.error('cronjob updateSpots bulk_update 트랜젝션 에러')


    if not resultDict:
        return
    url = "http://api.vworld.kr/req/address?service=address&request=getAddress&version=2.0&crs=epsg:4326&point={0},{1}&type=PARCEL&zipcode=false&simple=true&key={2}"
    for k, v in resultDict.items():
        trynum = 3 
        while trynum>0:
            try:
                requrl = url.format(str(v['stationLongitude']), str(v['stationLatitude']), API_KEY_vworld)
                request = urllib.request.Request(requrl)
                response = urllib.request.urlopen(request)
            except:
                logger.error('vworld api 호출 에러 : ' + url)
                trynum -= 1
                if trynum == 0:
                    raise exceptions.PermissionDenied('api에 접근할 수 없습니다.', code=403)
                continue
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                responseDict = json.loads(response_body.decode('utf-8'))
                code = responseDict['response']['status']
                if code=='NOT_FOUND':
                    v['stationLongitude'] = float(v['stationLongitude']) - 0.000001
                    v['stationLatitude'] = float(v['stationLatitude']) - 0.000001
                    continue
                if code=='ERROR':
                    logger.error('vworld api 에러. {0}'.format(responseDict['response']['service']['error']['text']))
                    print(responseDict['response']['error']['text'])
                    trynum-=1
                    continue
                vworldDict = responseDict['response']['result'][0]
                resultDict[k].update({"address" : vworldDict['text'], "district" : vworldDict["structure"]["level2"]})
                trynum=0
            else:
                print(rescode)
                trynum -= 1
                if trynum == 0:
                    raise exceptions.APIException('api에서 원하는 정보를 얻을 수 없습니다.', code=404)
                logger.warning('api 연결 에러로 다시 시도. 이후 남은 시도 : '+trynum)
                time.sleep(10)

    now = datetime.now()

    try:
        with transaction.atomic():  
            newBikeSpots = [models.Bikespot(idnumber=int(v['num']), spot_name=v['spotname'], district=v['district'], open_date=now, capacity=v['rackTotCnt'],
            latitude=v['stationLatitude'], longitude=v['stationLongitude'], address=v['address'], bike_number=v['parkingBikeTotCnt'], opened=True) 
            for k, v in resultDict.items() ]
            models.Bikespot.objects.bulk_create(newBikeSpots) 

    except IntegrityError as e:
        print(e)
        logger.error('cronjob updateSpots bulk_create 트랜젝션 에러')


def putHistoryDB(timestring):
    nowdate = int(timestring[:8])
    nowhour = int(timestring[8:])
    if models.BikeHistory.objects.filter(date=nowdate, hour=nowhour).exists():
        return
    logger.info('cron-history : '+timestring)   
    url = "http://openapi.seoul.go.kr:8088/{0}/json/bikeListHist/{1}/{2}/{3}"
    resultDict = {}
    for i in range(0, 3000, 1000):
        trynum = 3
        while trynum > 0:
            try:
                requrl = url.format(API_KEY_seoulbike, i+1, i+1000, timestring)
                request = urllib.request.Request(requrl)
                response = urllib.request.urlopen(request)
            except:
                logger.warning('cron-history api 호출 에러로 다시 시도. 남은 시도 : '+trynum)
                trynum -= 1
                if trynum == 0:
                    raise exceptions.PermissionDenied('cron-history api에 접근할 수 없습니다.', code=403)
                continue
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                responseDict = json.loads(response_body.decode('utf-8'))
                code = responseDict['getStationListHist']['RESULT']['CODE']
                if (code in ['INFO-100', 'ERROR-301', 'ERROR-310', 'INFO-200']):
                    logger.error('cron-history fetal error : url과 인증키, 또는 서비스 확인 요망. url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("url과 인증키, 또는 서비스 확인 요망", code=500)
                if (code in ['ERROR-300','ERROR-331', 'ERROR-332', 'ERROR-333', 'ERROR-334', 'ERROR-335', 'ERROR-336']):
                    logger.error('cron-history error : 잘못된 url : {}'.format(requrl))
                    trynum=0
                    raise exceptions.APIException("error : 잘못된 url", code=500)
                if (code in ['ERROR-500', 'ERROR-600', 'ERROR-601']):
                    trynum -= 1
                    if trynum == 0:
                        raise exceptions.APIException("error : 따릉이 대여소의 정보를 확인할 수 없습니다.", code=400)    
                    time.sleep(10)
                    logger.warning('cron-history api측 오류로 다시 시도. 이후 남은 시도 : '+trynum)
                    continue
                for spot in responseDict['getStationListHist']["row"]:
                    try:
                        num, _ = spot['stationName'].split('.', 1)
                        resultDict[int(num)] = int(spot['parkingBikeTotCnt'])
                    except:
                        continue
                trynum = 0
            else:
                trynum -= 1
                if trynum == 0:
                    raise exceptions.APIException('api에서 원하는 정보를 얻을 수 없습니다.', code=404)
                logger.warning('cron-history api 연결 에러로 다시 시도. 이후 남은 시도 : '+trynum)
                time.sleep(10)

    try:
        with transaction.atomic():        
            
            newHistories = [models.BikeHistory(date=nowdate, hour=nowhour, 
            spot=idnumber, have=resultDict[idnumber] ) 
            for idnumber in resultDict.keys() ]

            models.BikeHistory.objects.bulk_create(newHistories) 

    except IntegrityError as e:
        logger.error('cron-history 트랜젝션 에러')


def DBclear():  #DB정보 삭제하는 메소드
    pass 
    
def MakeModel(): #모델 훈련 파이프라인
    pass

def getWeatherForecast():      #맨처음 실행후 3시간마다 실행  0000, 0300, 0600, 0900, 1200, 1500, 1800, 2100
    
    
    now = datetime.now()  
    nowHour = int(str(now.hour).zfill(2))
    if nowHour < 2:
        now = now-timedelta(days=1)
        nowHour += 24
    basetime = (nowHour-3)//3*3+2  #basetime = 0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300 
    basetime = str(basetime).zfill(2)+'00'
    nx = 60 #lat = 37.5760612
    ny = 127 #lon = 126.9658593
    numOfRows = 12*60 #혹시모르므로 2일에 12시간 더 얹어서 가져옴
    baseDate = int(str(now.year)+str(now.month).zfill(2)+str(now.day).zfill(2))
    logger.info('cron-weather : {0}{1}'.format(baseDate, basetime))
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?dataType=json&serviceKey={0}&numOfRows={1}&pageNo=1&base_date={2}&base_time={3}&nx={4}&ny={5}"
    trynum = 3

    resultDict = {}
    while trynum > 0:
        try:
            requrl = url.format(API_KEY_weather, numOfRows, baseDate, basetime, nx, ny)
            request = urllib.request.Request(requrl)
            response = urllib.request.urlopen(request)
        except:
            logger.warning('cron-weather api 호출 에러로 다시 시도. 남은 시도 : '+trynum)
            trynum -= 1
            if trynum == 0:
                raise exceptions.PermissionDenied('api에 접근할 수 없습니다.', code=403)
            continue
        rescode = response.getcode()
        if(rescode!=200):
            trynum -= 1
            if trynum == 0:
                raise exceptions.APIException('api에서 원하는 정보를 얻을 수 없습니다.', code=404)
            logger.warning('cron-history api 연결 에러로 다시 시도. 이후 남은 시도 : '+trynum)
            time.sleep(10)
            continue
        else:
            response_body = response.read()
            responseDict = json.loads(response_body.decode('utf-8'))
            code = responseDict['response']['header']['resultCode']
            if (code in ['11','12','20','21','22','30','31','32','33']):
                logger.error('fetal error : url과 인증키, 또는 서비스 확인 요망. url : {}'.format(requrl))
                trynum=0
                raise exceptions.APIException("url과 인증키, 또는 서비스 확인 요망", code=500)
            if (code in ['03','04','10']):
                logger.error('error : 잘못된 url : {}'.format(requrl))
                trynum=0
                raise exceptions.APIException("error : 잘못된 url", code=500)
            if (code in ['01','02','05','99']):
                trynum -= 1
                if trynum == 0:
                    raise exceptions.APIException("error : 따릉이 대여소의 정보를 확인할 수 없습니다.", code=400)    
                time.sleep(10)
                logger.warning('api측 오류로 다시 시도. 이후 남은 시도 : '+trynum)
                continue
            for spot in responseDict['response']['body']["items"]['item']:
                datehour = spot['fcstDate'] + spot['fcstTime'][0:2]
                if spot['category'] not in ['PCP', 'REH', 'SNO', 'TMP']:
                    continue
                if datehour in resultDict:                    
                    resultDict[datehour].update({spot['category'] : spot['fcstValue']})
                else:
                    resultDict[datehour] = {spot['category'] : spot['fcstValue']}
                this.historyUpdated = True
            trynum = 0
    
    return resultDict         


                     
