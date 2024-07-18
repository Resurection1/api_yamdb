import random
import string

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import MyUser
from .serializers import TokenSerializer, UserSignupSerializer


class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            confirmation_code = ''.join(random.choices(
                string.ascii_letters + string.digits, k=6))
            user.confirmation_code = confirmation_code
            user.save()
            send_mail(
                'Your confirmation code',
                f'Your confirmation code is {confirmation_code}',
                'CuPKO1797@yandex.ru',
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = MyUser.objects.get(username=username)
                if user.confirmation_code == confirmation_code:
                    refresh = RefreshToken.for_user(user)
                    user.is_active = True
                    user.confirmation_code = ''
                    user.save()
                    return Response({'token': str(refresh.access_token)},
                                    status=status.HTTP_200_OK)
                return Response({'confirmation_code':
                                 ['Не верный код подтверждения.']},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            except MyUser.DoesNotExist:
                return Response({'username': ['Пользователь не найден.']},
                                status=status.HTTP_404_NOT_FOUND
                                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
