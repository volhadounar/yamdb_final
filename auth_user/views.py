from api_yamdb.settings import ADMIN_EMAIL

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import exceptions, filters, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.tokens import AccessToken

from .paginations import StandardResultsSetPagination
from .private_permissions import IsAdminRole
from .serializers import (ConfirmationSerializer, EmailSerializer,
                          UserSerializer)


User = get_user_model()


def send_msg(email, code):
    subject = 'Response with code confirmation'
    body = f'''
        {code}
    '''
    send_mail(
        subject, body, email, [ADMIN_EMAIL, ],
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_send_mail(request):
    email_serializer = EmailSerializer(data=request.data)
    email_serializer.is_valid(raise_exception=True)
    to = email_serializer.validated_data['email']
    username = to.split('@')[0]
    user, created = User.objects.get_or_create(email=to,
                                               username=username)
    code = default_token_generator.make_token(user)
    send_msg(to, code)
    return Response(email_serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    """Аутентификация пользователя. Выдача токена."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        confirmation = ConfirmationSerializer(data=request.data)
        confirmation.is_valid(raise_exception=True)
        email = confirmation.validated_data['email']
        confirmation_code = confirmation.data.get('confirmation_code')
        username = email.split('@')[0]
        user = get_object_or_404(User, email=email,
                                 username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            exceptions.AuthenticationFailed(
                'confirmation_code is not valid')

        serialized_user = UserSerializer(user).data

        access_token = AccessToken.for_user(user)

        response = Response()
        response.data = {
            'access_token': f'{access_token}',
            'user': serialized_user,
        }

        return response


class UserViewSet(ModelViewSet):
    """Управление профилем текущего пользователя
       и другими пользователями в системе."""
    permission_classes = [permissions.IsAuthenticated & IsAdminRole]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['email', 'name']

    @action(methods=['get', 'patch', 'put'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            obj = get_object_or_404(self.queryset,
                                    email=self.request.user.email)
            serializer = UserSerializer(obj)
            return Response(serializer.data)

        obj = get_object_or_404(self.queryset, email=self.request.user.email)
        serializer = UserSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
