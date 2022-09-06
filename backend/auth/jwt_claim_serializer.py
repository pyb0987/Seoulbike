from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import os

class TokenObtainPairSerializerWithInfo(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):   # database에서 조회된 user의 정보가 user로 들어오게 된다.
        token = super().get_token(user)

        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['image'] = os.path.join("http://localhost:8000/media", str(user.image))      # 로그인한 사용자의 클레임

        return token