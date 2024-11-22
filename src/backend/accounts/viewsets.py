import logging
from datetime import datetime, date, timedelta
from functools import partial

from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.core import signing
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from .models import PasswordResetCode, OTPLogin
from .filters import UserBasicFilter
from .permissions import UserPermissions
from .serializers import UserSerializer, PasswordResetSerializer, UserBasicDataSerializer, \
    CustomerRegistrationSerializer
from .services import auth_login, auth_password_change, auth_register_user, _parse_data, auth_login_employee, \
    user_clone_api, get_user_from_email_or_mobile_or_employee_code, generate_auth_data, customer_user_clone_api, \
    auth_login_customer
from ..base import response
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.serializers import SawaggerResponseSerializer
from ..base.services import create_update_record
from ..customer.filters import CustomerFilter
from ..customer.models import Customer
from ..customer.services import get_customer_user_obj
from ..employee.services import get_current_court, get_employee_obj
from ..base.utils.sms import send_sms

logger = logging.getLogger(__name__)

parse_password_reset_data = partial(_parse_data, cls=PasswordResetSerializer)


class UserViewSet(ModelViewSet):
    """
    Here we have user login, logout, endpoints.
    """
    queryset = get_user_model().objects.all()
    permission_classes = (UserPermissions,)
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(UserViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = UserBasicFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="post",
        operation_summary='Login',
        operation_description='Post login credential to log in and get a login session token.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="mobile/email/employee_code"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Logged In'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def login(self, request):
        return auth_login(request)

    # @action(detail=False, methods=['POST'])
    # def superuser_login(self, request):
    #     return auth_login_superuser(request)

    @swagger_auto_schema(
        method="post",
        operation_summary='Login',
        operation_description='Post login credential to log in and get a login session token.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="mobile/email/employee_code"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Logged In'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def employee_login(self, request):
        return auth_login_employee(request)

    @swagger_auto_schema(
        method="post",
        operation_summary='Login',
        operation_description='Post login credential to log in and get a login session token.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="mobile/email/employee_code"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Logged In'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def customer_login(self, request):
        return auth_login_customer(request)

    @action(methods=['GET'], detail=False)
    def user_clone(self, request):
        if not request.user.is_authenticated:
            content = {'detail': 'user is not authenticated'}
            return response.Unauthorized(content)
        if request.user.is_separated:
            content = {'detail': 'user is separated from the system'}
            return response.Unauthorized(content)
        court = get_current_court(request)
        employee = get_employee_obj(request.user.pk, court)
        return response.Ok(user_clone_api(request.user, employee))


    @action(methods=['GET'], detail=False)
    def customer_clone(self, request):
        if not request.user.is_authenticated:
            content = {'detail': 'user is not authenticated'}
            return response.Unauthorized(content)
        if request.user.is_separated:
            content = {'detail': 'user is separated from the system'}
            return response.Unauthorized(content)
        customer = get_customer_user_obj(request.user.pk)
        return response.Ok(customer_user_clone_api(request.user, customer))

    @swagger_auto_schema(
        method="post",
        operation_summary='Change Password',
        operation_description='Post old and new password while logged in session.',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Password changed Successfully.'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def password_change(self, request):
        data = auth_password_change(request)
        user, new_password = request.user, data.get('new_password')
        if new_password:
            if len(new_password) < 6:
                return response.BadRequest({"detail": "Password too short."})
        if user.check_password(data.get('old_password')):
            user.set_password(new_password)
            user.save()
            content = {'success': 'Password changed successfully.'}
            return response.Ok(content)
        else:
            content = {'detail': 'Old password is incorrect.'}
            return response.BadRequest(content)

    @swagger_auto_schema(
        method="post",
        operation_summary='Send Password Reset Mail',
        operation_description='Post username to get a code on mail to make new password using reset_password API. Used in case of forget password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="mobile/email/employee_code"),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Password changed Successfully.'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def user_reset_mail(self, request):
        data = parse_password_reset_data(request.data)
        username = data.get('username')
        is_employee = data.get('is_employee', False)
        user, email_user, mobile_user, username_user = get_user_from_email_or_mobile_or_employee_code(username)
        if not email_user and not mobile_user and not username_user:
            return response.BadRequest({'detail': 'User does not exists.'})
        if user:
            try:
                email = user.email
                password_reset_code = PasswordResetCode.objects.create_reset_code(user)
                password_reset_code.send_password_reset_email(is_employee=is_employee)
                message = "We have sent a password reset link to the {}. Use that link to set your new password".format(
                    email)
                return response.Ok({"detail": message})
            except get_user_model().DoesNotExist:
                message = "Email '{}' is not registered with us. Please provide a valid email id".format(email)
                message_dict = {'detail': message}
                return response.BadRequest(message_dict)
            except Exception:
                message = "Unable to send password reset link to email-id- {}".format(email)
                message_dict = {'detail': message}
                logger.exception(message)
                return response.BadRequest(message_dict)
        else:
            message = {'detail': 'User for this staff does not exist'}
            return response.BadRequest(message)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        data = auth_register_user(request)
        return response.Created(data)

    @swagger_auto_schema(
        method="post",
        operation_summary='Reset Password',
        operation_description='Use the code got in mail by using reset_password_mail API to make new password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, description="code received on mail"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description=""),
            }),
        responses={
            200: SawaggerResponseSerializer(data={'message': 'Password changed Successfully.'}, partial=True)
        }
    )
    @action(detail=False, methods=['POST'])
    def reset_password(self, request):
        code = request.data.get('code')
        password = request.data.get('password')
        if code:
            try:
                password_reset_code = PasswordResetCode.objects.get(code=code.encode('utf8'))
                uid = force_str(urlsafe_base64_decode(password_reset_code.uid))
                password_reset_code.user = get_user_model().objects.get(id=uid)
            except:
                message = 'Unable to verify user.'
                message_dict = {'detail': message}
                return response.BadRequest(message_dict)
            # verify signature with the help of timestamp and previous password for one secret urls of password reset.
            else:
                signer = signing.TimestampSigner()
                max_age = settings.PASSWORD_RESET_TIME
                l = (password_reset_code.user.password, password_reset_code.timestamp, password_reset_code.signature)
                try:
                    signer.unsign(':'.join(l), max_age=max_age)
                except (signing.BadSignature, signing.SignatureExpired):
                    logger.info('Session Expired')
                    message = 'Password reset link expired. Please re-generate password reset link. '
                    message_dict = {'detail': message}
                    return response.BadRequest(message_dict)
            password_reset_code.user.set_password(password)
            password_reset_code.user.save()
            message = "Password Created successfully"
            message_dict = {'detail': message}
            return response.Ok({"success": message_dict})
        else:
            message = {'detail': 'Password reset link expired. Please re-generate password reset link. '}
            return response.BadRequest(message)

    @action(detail=False, methods=['POST'])
    def resend_otp(self, request):
        import datetime
        mobile = request.data.get("mobile")
        if mobile:
            timestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
            login_obj = OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=timestamp,
                                                resend_counter__gt=0).first()
            if login_obj:
                is_sent, detail = send_sms(mobile, "Your CA Cloud Desk OTP is " + str(
                    login_obj.otp) + ". Keep OTPs secret. Don't share with anyone. CA Cloud Desk Team Law Seva")
                if not is_sent:
                    return response.BadRequest(detail)
                login_obj.resend_counter = login_obj.resend_counter - 1
                login_obj.save()
                return response.Ok({"detail": "OTP resent successfully"})
            else:
                return response.BadRequest(
                    {"detail": "Maximum retries have been exceeded. Please retry after 15 minutes."})
        else:
            return response.BadRequest({"detail": "Mobile is required!"})

    @action(detail=False, methods=['POST'])
    def send_otp(self, request):
        mobile = request.data.get("mobile")
        if mobile:
            otp = self.get_random_number(6)
            OTPLogin.objects.filter(mobile=mobile, modified_at__lt=date.today(), is_active=True).delete()
            login_obj = OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=date.today()).first()
            if login_obj:
                counter = login_obj.counter - 1
                if counter > 0:
                    OTPLogin.objects.filter(mobile=mobile, is_active=True, modified_at__gte=date.today()).update(
                        otp=otp, is_active=True, counter=counter, resend_counter=25, modified_at=datetime.now())
            else:
                counter = 25
                OTPLogin.objects.create(mobile=mobile, otp=otp)
            if counter > 0:
                is_sent, detail = send_sms(mobile, "Your CA Cloud Desk OTP is " + str(
                    otp) + ". Keep OTPs secret. Don't share with anyone. CA Cloud Desk Team Law Seva")
                if not is_sent:
                    return response.BadRequest(detail)
                return response.Ok({"detail": "OTP sent successfully"})
            else:
                return response.BadRequest(
                    {"detail": "Max tries for OTP exceeded. Kindly try again tommorow or login with password"})
        else:
            return response.BadRequest({"detail": "Mobile is required!"})

    @action(detail=False, methods=['POST'])
    def verify_otp(self, request):
        mobile = request.data.get("mobile")
        otp = request.data.get("otp")
        user_model = get_user_model()
        user = user_model.objects.filter(is_active=True, mobile=mobile).first()
        if user:
            timestamp = datetime.now() - timedelta(minutes=15)
            login_obj = OTPLogin.objects.filter(mobile=mobile, otp=otp, is_active=True,
                                                modified_at__gte=timestamp).first()
            if login_obj:
                login_obj.is_active = False
                login_obj.save()
                auth_data = generate_auth_data(request, user)
                return response.Ok(auth_data)
            else:
                return response.BadRequest({"detail": "Invalid OTP used. Please Check!!"})
        else:
            return response.BadRequest({"detail": "No Such User with mobile no: " + str(mobile) + " exists."})

    @action(methods=['GET'], detail=False, pagination_class=StandardResultsSetPagination)
    def admin_list(self, request):
        queryset = get_user_model().objects.filter(is_active=True, is_separated=False)
        queryset = queryset.filter(is_superuser=True)
        queryset = queryset.order_by('first_name', 'last_name')
        self.filterset_class = UserBasicFilter
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(UserBasicDataSerializer(page, many=True).data)
        return response.Ok(UserBasicDataSerializer(queryset, many=True).data)

    @action(methods=['GET'], detail=False, pagination_class=StandardResultsSetPagination)
    def employee_list(self, request):
        queryset = get_user_model().objects.filter(is_active=True, is_separated=False, is_superuser=False)
        queryset = queryset.order_by('first_name', 'last_name')
        self.filterset_class = UserBasicFilter
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(UserBasicDataSerializer(page, many=True).data)
        return response.Ok(UserBasicDataSerializer(queryset, many=True).data)

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Customer',
        operation_description='Add Customer',
        request_body=CustomerRegistrationSerializer,
        response=CustomerRegistrationSerializer
    )
    @action(methods=[ 'POST'], detail=False, queryset=Customer, filterset_class=CustomerFilter)
    def customer_register(self, request):
        data = auth_register_user(request)
        request_data = request.data.copy()
        first_name = request_data.get("first_name", "")
        middle_name = request_data.get("middle_name", "")
        last_name = request_data.get("last_name", "")
        request_data["name"] = f"{first_name} {middle_name} {last_name}".strip()
        request_data["user"] = data["id"]
        return response.Ok(create_update_record(request_data, CustomerRegistrationSerializer, Customer))
