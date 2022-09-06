
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .jwt_claim_view import TokenObtainPairViewWithInfo
from django.urls import path, include
from . import views
app_name = 'auth'


urlpatterns = [
    path('access/', TokenRefreshView.as_view(), name='token_get_access'),
    path('both/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('info/', TokenObtainPairViewWithInfo.as_view(), name='token_obtain_info'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'))

    
]