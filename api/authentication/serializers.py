from datetime import timedelta
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.exceptions import APIException, NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.utils.timezone import now

from ghasedakpack import Ghasedak
from phonenumber_field.serializerfields import PhoneNumberField
from pyotp import TOTP

from api.users.models import User, UserOtp

class SendOtp(Serializer):
    phone_number = PhoneNumberField(required=True)

    def save(self):
        # Get/Create a user
        user, _ = User.objects.get_or_create(username=self.validated_data['phone_number'])

        # Throttle the endpoint
        recently = now() - timedelta(seconds=settings.OTP_EXPIRE_TIME)
        if UserOtp.objects.filter(user=user, otp_at__gte=recently).exists():
            raise APIException(f'You should wait {(UserOtp.objects.filter(user=user, otp_at__gte=recently).first().otp_at - recently).seconds} seconds to send another otp', 'otp_sms_throttle')

        # Generate OTP
        user_otp, _  = UserOtp.objects.update_or_create(user=user, defaults={'otp_at': now()})
        otp = TOTP(user.key, interval=settings.OTP_EXPIRE_TIME).at(user_otp.otp_at)

        # Send OTP
        ghasedak = Ghasedak(settings.GHASEDAK_API_KEY)
        if not ghasedak.verification({
                'receptor': str(self.validated_data['phone_number']),
                'type': Ghasedak.SMS_TYPE,
                'template': settings.OTP_TEMPLATE_NAME,
                'param1': otp
            }):
            raise APIException('There was an error with ghasedak api', 'ghasedak')

class SignInOtp(Serializer):
    phone_number = PhoneNumberField(required=True)
    otp = serializers.CharField(required=True)
    bypass = serializers.BooleanField(default=False)
    
    def validate(self, data):
        if not User.objects.filter(is_active=True, username=data['phone_number']).exists():
            raise NotFound('User with the specified phone_number was not found')
        return super().validate(data)

    def sign_in(self):
        user = User.objects.get(username=self.validated_data['phone_number'])
        bypass =  settings.DEBUG and self.validated_data['bypass']

        if bypass or user.verify_otp(self.validated_data['otp']):
            user.last_login = now()
            user.save()
            token = RefreshToken.for_user(user)
            return {
                'access': str(token.access_token),
                'refresh': str(token)
            }
        else:
            raise APIException('Provided otp is not valid', 'invalid_otp')