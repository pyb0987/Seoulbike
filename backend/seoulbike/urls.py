from django.urls import include, path
from rest_framework import routers
from . import views
from . import modelAPI

app_name = 'seoulbike'

router = routers.DefaultRouter()
router.register('user', views.UserViewset)
router.register('bikespot', views.BikespotViewset)
router.register('review', views.ReviewViewset)

router.register('admin/user', views.AdminUserViewset)
router.register('admin/bikespot', views.BikespotViewset)
router.register('admin/review', views.AdminReviewViewset)

urlpatterns = [
     path('models', modelAPI.Models),
     path('<slug:model>/field', modelAPI.ModelField),
     path('<slug:model>/file', modelAPI.fileUpload),
     path('cronjob/current', modelAPI.getBikeNum),
     path('cronjob/updateSpots', modelAPI.updateSpots),
     path('cronjob/history', modelAPI.getAllBikeHistory),
     path('', include(router.urls)),
 

    
]