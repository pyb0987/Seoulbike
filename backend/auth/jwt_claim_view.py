from .jwt_claim_serializer import TokenObtainPairSerializerWithInfo
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenObtainPairViewWithInfo(TokenObtainPairView):
    # serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
    serializer_class = TokenObtainPairSerializerWithInfo