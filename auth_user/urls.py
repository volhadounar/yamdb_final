from auth_user.views import LoginView, UserViewSet, api_send_mail

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/auth/email/', api_send_mail),
    path('v1/auth/token/', LoginView.as_view(), name='token_obtain'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh')
]

urlpatterns += [
    path('v1/', include(router.urls)),
]
