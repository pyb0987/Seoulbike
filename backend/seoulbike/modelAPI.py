from rest_framework.decorators import renderer_classes, api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.http import JsonResponse
from django.apps import apps 
from django.db import transaction, IntegrityError
from datetime import datetime, timedelta


from . import models
from . import cron
import pandas as pd
import io
import logging
import chardet
import json

 
logger = logging.getLogger('seoulbike')


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def Models(request):
    modelsType = [name.__name__ for name in apps.get_models(include_auto_created=False, include_swapped=False)]
    modelsType.remove('LogEntry')
    modelsType.remove('Permission')
    modelsType.remove('Group')
    modelsType.remove('ContentType')
    modelsType.remove('Session')
    modelsType.remove('BikeHistory')
    modelsType.remove('ResetPasswordToken')
    return JsonResponse(modelsType,safe=False)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def ModelField(request, model = ''):
    if model=='':
        logger.warning('잘못된 방식으로 관리자 페이지에 접근 시도')
        return Response("Parameter Invalid", status=status.HTTP_400_BAD_REQUEST)
    try:
        fields = getattr(models, model.capitalize())._meta.get_fields(include_hidden=False) #include_parents=True, 
        modelField = [field.name for field in fields]
    except:
        logger.warning('잘못된 방식으로 관리자 페이지에 접근 시도')
        return Response("Paramter Not Found", status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(modelField,safe=False)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def fileUpload(request, model = ''):
    if model=='':
        return Response("파라미터가 유효하지 않습니다.", status=status.HTTP_400_BAD_REQUEST)
    for mdl in apps.get_models(include_auto_created=False, include_swapped=False):      #대상이 되는 모델 확인
        if model == mdl.__name__.lower():
            selectedModel = mdl
            break
    else:
        logger.warning('잘못된 방식으로 모델 접근')
        return Response("대상이 되는 모델을 확인할 수 없습니다.", status=status.HTTP_404_NOT_FOUND)
        
    payload = request.FILES
    fieldmap = request.data['field']
    fieldmap = json.loads(fieldmap)
    file_object = payload['files']
    fileread =file_object.read()
    try:
        fileEncoder = chardet.detect(fileread)['encoding']      #encode 찾아서 엔코딩
        fileRead = io.StringIO(fileread.decode(fileEncoder))
        fileRead.seek(0)
        df = pd.read_csv(fileRead, delimiter=',')
    except Exception as e:
        logger.warning('읽을 수 없는 인코딩 파일')
        return Response(str(e), status=415)
    for key in fieldmap.keys():
        
        if fieldmap[key]['required']:
            if fieldmap[key]['label'] not in df.columns:            #있어야 할 항목이 채워져있는지 확인
                return Response('필수 컬럼 중 없는 컬럼이 있습니다.', status=status.HTTP_400_BAD_REQUEST)   
            if df[fieldmap[key]['label']].isna().sum() > 0:
                return Response('필수 컬럼 중 없는 항목이 있습니다.', status=status.HTTP_400_BAD_REQUEST)             
    newColumnDict = {}
    for key in fieldmap.keys():                 #실제 field에 들어가야 할 이름으로 변경
        newColumnDict[fieldmap[key]['label']] = fieldmap[key]['name']
    df.rename(columns=newColumnDict, inplace=True)

    ModelField = [field.name for field in selectedModel._meta.get_fields(include_hidden=False)]  #대상이 되는 모델의 칼럼 추출
    dropColumn = []
    for column in df.columns:                 #실제 field에 들어가지 않는 칼럼들을 삭제
        if column not in ModelField:
            dropColumn.append(column)
    df.drop(dropColumn, axis=1, inplace=True)
      
    try:
        with transaction.atomic():  
            selectedModel.objects.bulk_create([
                selectedModel(**(rowfields.dropna().to_dict())) for index, rowfields in df.iterrows()
            ])           
            successNum = len(df)
    except IntegrityError as e:
        logger.info('파일 업로드 트랜젝션 에러')
        return Response(str(e).split("\"")[1], status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    return JsonResponse(successNum,safe=False)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def getBikeNum(request):
    cron.getBikeNum()
    return JsonResponse({'data' : 1},safe=False)


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def updateSpots(request):
    cron.updateSpots()
    return JsonResponse({'data' : 1},safe=False)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAdminUser])
def getAllBikeHistory(request):

    now = datetime.now()
    for i in range(217):
        eachtime = now-timedelta(hours=217-i)
        timestring = str(eachtime.year)+str(eachtime.month).zfill(2)+str(eachtime.day).zfill(2)+str(eachtime.hour).zfill(2)
        print(timestring)
        cron.putHistoryDB(timestring)

          
    return JsonResponse({'data' : 1},safe=False)



