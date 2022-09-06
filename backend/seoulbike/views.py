from requests import delete
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import *
from . import models
from django.db.models import Q
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication
from rest_framework.permissions import IsAdminUser
from .permissions import IsAdminUserOrReadOnly, IsAuthenticatedOrReadAndWrite
import bcrypt
import datetime
from django.db.models import Count
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .buildAnalysis import Forecast


forecast = Forecast()

class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 50
    
class AdminReviewViewset(viewsets.ModelViewSet):
    pagination_class = Pagination
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = (JWTStatelessUserAuthentication,)
    permission_classes = [IsAdminUser]

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        del data['id']
        del data['user']
        review = self.get_object()

        serializer = ReviewSerializer(review, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminUserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search','')
        if search:
            qs = qs.filter(Q(username__icontains=search) | Q(email__icontains=search) | Q(user_spots__icontains=search) | 
            Q(first_name__icontains=search) | Q(last_name__icontains=search)  ).distinct()#.order('-student_id')
        return qs

    def partial_update(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            data = request.data
        else:
            data = request.data.dict()
        user = self.get_object()
        if 'user_spots' in data:
            if data['user_spots']=='':
                del data['user_spots']
            else:
                user_spots = data['user_spots']
                user_spots = list(user_spots.split(', '))
                data['user_spots'] = user_spots
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)    

class UserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    permission_classes = [IsAuthenticatedOrReadAndWrite]


    def partial_update(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            data = request.data
        else:
            data = request.data.dict()
        user = self.get_object()
        if 'user_spots' in data:
            user_spots = data['user_spots']
            user_spots = list(user_spots.split(', '))
            data['user_spots'] = user_spots
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search','')
        if search:
            qs = qs.filter(Q(username__icontains=search) | Q(email__icontains=search) | Q(user_spots__icontains=search) | 
            Q(first_name__icontains=search) | Q(last_name__icontains=search)  ).distinct()#.order('-student_id')
        return qs
    

    def create(self, request):
        if request.method == 'POST':
            password = request.data.get('password')
            confirmation = request.data.get('confirmation')
            if password != confirmation:
                return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            data = request.data.dict()
            user_spots = data['user_spots']
            if user_spots !='':
                user_spots = list(user_spots.split(', '))
                data['user_spots'] = user_spots
            else:
                del data['user_spots']
            if data['image'] =='':
                del data['image']
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(password)
                user.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': '접근할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, methods=['GET'])
    def namecheck(self, request):
        username = request.GET.get('username')
        print(username)
        try:
            user = models.User.objects.get(username=username)
            returnVal = 0
        except:
            user = None
            returnVal = 1
        return Response({"checked" : returnVal}, status=status.HTTP_200_OK) 


    @action(detail=True, methods=['GET', 'PUT'])
    def spots(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.method == 'GET':
            user_spots = user.user_spots.all()
            serializer = BikespotSerializer(user_spots, many=True)
            return Response(serializer.data)
        if request.method == 'PUT':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({'error': '잘못된 접근입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['PUT'])
    def change_pw(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if request.method == "PUT":
            data = request.data
            origin_password = data["password"]
            if check_password(origin_password,user.password):
                new_password = data["new_password"]
                new_confirmation = data["new_confirmation"]
                if new_password == new_confirmation:
                    user.set_password(new_password)
                    user.save()
                    auth_login(request,user)
                    return Response({'data' : '1'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '새로운 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': '잘못된 접근입니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def partial_update(self, request, *args, **kwargs):
        if request.content_type == "application/json":
            data = request.data
        else:
            data = request.data.dict()
        user = self.get_object()
        password = data['password']
        confirmation = data['confirmation']
        if password != confirmation:
            return Response({'error': '비밀번호와 비밀번호 확인 필드가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password,user.password):
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        if 'user_spots' in data:
            user_spots = data['user_spots']
            user_spots = list(user_spots.split(', '))
            data['user_spots'] = user_spots
        del data['password']
        del data['confirmation']
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = request.data
        password = data['password']
        confirmation = data['confirmation']
        user = self.get_object()
        if password != confirmation:
            return Response({'error': '비밀번호와 비밀번호 확인 필드가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password,user.password):
            return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        user.is_active = False
        user.image = ''
        user.email = ''
        user.user_spots.set([])
        user.save()
        return Response({'data' : 1}, status=status.HTTP_204_NO_CONTENT)

class BikespotViewset(viewsets.ModelViewSet):
    pagination_class = Pagination
    queryset = models.Bikespot.objects.all()
    serializer_class = BikespotSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search','')
        opened = self.request.query_params.get('opened','')

        if opened:
            opened = bool(opened)
            qs = qs.filter(Q(opened=opened))
        if search:
            qs = qs.filter(Q(idnumber__icontains=search) | Q(spot_name__icontains=search) | Q(address__icontains=search)).distinct()
        qs = qs.annotate(Count('spot_review', distinct=True)).order_by('-spot_review__count')
        return qs
    
    
    @action(detail=False, methods=['GET'])
    def all(self, request):
        qs = super().get_queryset()
        all_bikespots = qs.filter(opened=True)
        serializer = self.get_serializer(all_bikespots, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET'])
    def analysis(self, request, pk):
        fcst = forecast.getForecast(pk)
        return Response(fcst)

    




class ReviewViewset(viewsets.ModelViewSet):
    pagination_class = Pagination
    queryset = models.Review.objects.all()
    serializer_class = ReviewShowSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            idnumber = self.request.query_params.get('idnumber','')
            idnumber = int(idnumber)
            qs = qs.filter(target_spot__exact=idnumber).select_related('user').order_by('-create_date')
            return qs
        except:
            return qs

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = request.data.copy()
            if data['user'] is None:
                new_salt = bcrypt.gensalt() 
                password = data.pop('password')
                hashed_password = bcrypt.hashpw(password.encode('utf-8'),new_salt)
                hashed_password = hashed_password.decode('utf-8')
                data['password'] = hashed_password
            else:
                pass
            serializer = ReviewSerializer(data=data)
            if serializer.is_valid():
                review = serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': '접근할 수 없습니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


    @action(detail=False, methods=['GET'])
    def pwcheck(self, request):
        id = request.GET.get('id')
        password = request.GET.get('password')
        try:
            review = models.Review.objects.get(id=id)
        except:
            return Response({'error': '대상 리뷰가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        returnNum = bcrypt.checkpw(password.encode('utf-8'),review.password.encode('utf-8'))
        if returnNum==True:
            returnVal = 1
        else:
            returnVal = 0
        return Response({"checked" : returnVal}, status=status.HTTP_200_OK) 


    def destroy(self, request, *args, **kwargs):
        data = request.data.copy()
        review = self.get_object()
        if 'password' in data:
            password = data.pop('password')
            checkPassword = bcrypt.checkpw(password.encode('utf-8'),review.password.encode('utf-8'))
            if checkPassword==False:
                return Response({'error': '비밀번호가 변경되었거나 틀립니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            username = data.pop('username')
            if username!=str(review.user):
                return Response({'error': '다른 작성자의 댓글을 삭제할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)


    def partial_update(self, request, *args, **kwargs):
        
        data = request.data.copy()
        review = self.get_object()
        if 'password' in data:
            password = data.pop('password')
            username = data.pop('username')
            checkPassword = bcrypt.checkpw(password.encode('utf-8'),review.password.encode('utf-8'))
            if checkPassword==False:
                return Response({'error': '비밀번호가 변경되었거나 틀립니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            username = data.pop('username')

            if username!=str(review.user):
                return Response({'error': '다른 작성자의 댓글을 변경할 수 없습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ReviewSerializer(review, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        review.update_date = datetime.datetime.now()
        review.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


