from email.policy import default
from rest_framework import serializers
from .models import User, Bikespot, Review



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id","username", "password","is_active", "last_name", "first_name", "email", "date_joined", "user_spots", 'image']
    
    def get_user_spots(self, obj):
        print('get_user_spots', obj)
        user_spots = list(map(int, obj[0].split(', '))) 
        return user_spots
    def set_user_spot(self, obj):
        print('set_user_spot', obj)
        return obj
   
class UserInfoSerializer(serializers.ModelSerializer):
    #user_spots = serializers.PrimaryKeyRelatedField(queryset=Bikespot.objects.all(), many=True)


    class Meta:
        model = User
        fields = ["username","user_spots", 'image']
    


class BikespotSerializer(serializers.ModelSerializer):
    review_count = serializers.ReadOnlyField(source='spot_review__count', read_only=True)
    class Meta:
        model = Bikespot
        fields = ["address","spot_name", "bike_number", "capacity", "district", "idnumber", "latitude", "longitude", "open_date", "opened", "review_count"]



class ReviewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, allow_blank=True, write_only=True)
    
    
    class Meta:
        model = Review
        fields = '__all__'

class ReviewShowSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'target_spot', 'create_date', 'update_date', 'content', 'user']
