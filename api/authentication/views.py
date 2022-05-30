from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from .serializers import SendOtp, SignInOtp

class OtpViewSet(GenericViewSet):

    permission_classes = []

    @action(methods=['get'], detail=False, url_path='(?P<phone_number>[^/.]+)', serializer_class=SendOtp)
    def send(self, request, phone_number, *args, **kwargs):
        
        serializer = self.get_serializer(data={'phone_number':phone_number})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('ok', status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=False, serializer_class=SignInOtp)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.sign_in(), status=status.HTTP_200_OK)


class AuthViewSet(GenericViewSet):

    permission_classes = []

    @action(methods=SAFE_METHODS, detail=False)
    def status(self, request, *args, **kwargs):
        if bool(request.user and request.user.is_authenticated):
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

