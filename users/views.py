from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
# from auth.custome_auth import CustomBasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10


class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email__iexact=email).first()  # Case-insensitive lookup
        if not user or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=HTTP_400_BAD_REQUEST)

        # Generate JWT token with a custom expiration time
        refresh = RefreshToken.for_user(user)
        refresh = RefreshToken.for_user(user)
    
        # refresh.access_token.set_exp(str(timedelta(days=7)))

        serializer = self.get_serializer(user)
        return Response({'user': serializer.data, 'access-token': str(refresh.access_token),'refresh-token':str(refresh)})
    

class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=400)
        try:
            # Attempt to validate and refresh the refresh token
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            # Extend the expiration time of the access token
            # access_token.set_exp(str(timedelta(days=7)))
            return Response({'access-token': str(access_token)})
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid refresh token'}, status=400)


class SearchUserView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination 
    permission_classes = [IsAuthenticated] 
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return Response({'error': 'Keyword is required'}, status=HTTP_400_BAD_REQUEST)
        return User.objects.filter(Q(email__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
