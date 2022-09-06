


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import os
from uuid import uuid4


def date_upload_name(instance, filename):
    ymd_path = timezone.now().strftime('%Y/%m/%d') 
    uuid_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([ymd_path, uuid_name + extension])


class Bikespot(models.Model):
    idnumber = models.IntegerField(primary_key=True)
    spot_name = models.CharField(max_length=50)
    district = models.CharField(max_length=20)
    open_date = models.DateField()
    capacity = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField() #위도
    longitude = models.FloatField() #경도
    address = models.CharField(max_length=100)
    bike_number = models.IntegerField(default=0, blank=True)
    opened = models.BooleanField(default=True)



class User(AbstractUser):
    image = models.ImageField(upload_to=date_upload_name, default='image/placeholder.jpg')
    is_active = models.BooleanField(default=True)
    user_spots = models.ManyToManyField(Bikespot, null=True, blank=True, related_name='user_bikespot')
    

    


class Review(models.Model):
    target_spot = models.ForeignKey(Bikespot, on_delete=models.CASCADE, related_name='spot_review')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(null=True, blank=True)
    content = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_review')
    password = models.CharField(max_length=200, null=True, blank=True, default='')

class BikeHistory(models.Model): #['기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수', '경과도', '2020년', '광도', '출근',
       #'퇴근', '유출량(-49)', '유출량(-72)', '유출량(-73)', '유출량(-96)', '유출량(-97)',
       #'유출량(-120)', '유출량(-121)', '유출량(-144)', '유출량(-145)', '유출량(-168)',
       #'유출량(-169)', '유출량(-192)', '유출량(-193)', '유출량(-216)', '월_1', '월_2', '월_3',
       #'월_4', '월_5', '월_6', '월_7', '월_8', '월_9', '월_10', '월_11', '월_12', '시_0',
       #'시_1', '시_2', '시_3', '시_4', '시_5', '시_6', '시_7', '시_8', '시_9', '시_10',
       #'시_11', '시_12', '시_13', '시_14', '시_15', '시_16', '시_17', '시_18', '시_19',
       #'시_20', '시_21', '시_22', '시_23']
    date = models.IntegerField()
    hour = models.IntegerField()
    spot = models.IntegerField()
    have = models.IntegerField()  #outflow = have - have(+1)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'hour', 'spot'], name='history_unit'
            )
        ]


##########################################


