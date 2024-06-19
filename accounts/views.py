from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.models import *
from accounts.serializers import *

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogoutView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                'message': 'You are logged out'
            }
            return Response(data, status=205)
        except TokenError:
            return Response(status=400)


class ChangeUserInfoView(UpdateAPIView):
    serializer_class = ChangeUserInformation
    http_method_names = ['patch', 'put']

    def get_object(self):
         return self.request.user


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return self.request.user


    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=400)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            data = {
                'success': True,
                'message': 'Password updated successfully',
            }
            return Response(data, status=200)
        return Response(serializer.errors, status=400)
