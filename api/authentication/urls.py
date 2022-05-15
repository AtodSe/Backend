from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import OtpViewSet, AuthViewSet


router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')
router.register(r'otp', OtpViewSet, basename='otp')

urlpatterns = router.urls

urlpatterns += [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
