import json
import base64
from decouple import config
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from django.core.files.base import ContentFile
from .constants import SETTINGS_CONSTANT, CORE_SERVICES, NON_CORE_SERVICES
from .filters import DynamicSettingsFilter, CountryFilter, StateFilter, CityFilter, CourtFilter, EmployeeFilter, \
    DescriptionTemplateFilter
from .models import DynamicSettings, Country, State, City, Court, Employee, UploadedDocument, DescriptionTemplate
from .permissions import DynamicSettingsPermissions, UploadedDocumentPermissions
from .serializers import DynamicSettingsSerializer, CountrySerializer, StateSerializer, CitySerializer, CourtSerializer, \
    UploadedDocumentSerializer, DescriptionTemplateSerializer, CourtBasicDataSerializer, \
    CourtDataSerializer, DeleteEmployeeSerializer, EmployeeSerializer
from .services import dropdown_tree, create_new_user
from ..accounts.filters import UserBasicFilter
from ..accounts.serializers import UserSerializer
from ..base.utils.email import send_from_template
from ..base import response
from ..base.api.pagination import StandardResultsSetPagination
from ..base.api.viewsets import ModelViewSet
from ..base.services import create_update_record, create_update_bulk_records, bytes_to_mb, gb_to_bytes


class UploadedDocumentViewSet(ModelViewSet):
    serializer_class = UploadedDocumentSerializer
    queryset = UploadedDocument.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = (UploadedDocumentPermissions,)
    parser_classes = (JSONParser, MultiPartParser)

    def get_queryset(self):
        queryset = super(UploadedDocumentViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset.order_by('-id')

    @action(methods=['POST'], detail=False)
    def create_with_base64(self, request):
        data = request.data.copy()
        img_format, imgstr = data['image'].split(';base64,')
        ext = img_format.split('/')[-1]
        data['image'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        serializer = UploadedDocumentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Ok(serializer.data)

    @action(methods=['POST'], detail=False)
    def multiple(self, request):
        data = {"is_active": True}
        result = []
        req_data = json.loads(base64.b64decode(request.data['images']))
        for obj in req_data:
            img_data = obj.get('data', None)
            img_name = obj.get('path', None)
            if img_data and img_name:
                data['image'] = ContentFile(base64.b64decode(img_data), name=img_name.split("/")[-1])
                data['name'] = img_name.split("/")[-1]
                serializer = UploadedDocumentSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                result.append(serializer.data)
        return response.Ok(result)

    # @action(methods=['POST'], detail=False)
    # def presigned_url(self, request):
    #     req_data = request.data.copy()
    #     is_personal = req_data.get('is_personal', False)
    #     if is_personal:
    #         file_size = PersonalFiles.objects.filter(user=request.user.pk, is_active=True).aggregate(
    #             Sum('file_size', output_field=FloatField()))
    #         file_size = file_size.get('file_size__sum', 0)
    #         if bytes_to_mb(file_size) > request.user.personal_storage:
    #             return response.BadRequest({'detail': 'Your storage is full, please contact ' + config(
    #                 'COMPANY_EMAIL') + ' to increase storage!'})
    #     Court = get_current_Court(request)
    #     if Court:
    #         file_size = Files.objects.filter(is_active=True, file_size__isnull=False).aggregate(
    #             Sum('file_size', output_field=FloatField()))
    #         file_size = file_size.get('file_size__sum', 0)
    #         queryset = CourtPlan.objects.filter(Court=Court, is_completed=True, is_active=True)
    #         queryset = get_active_plans(queryset)
    #         queryset = queryset.order_by('plan__end_size').first()
    #         plan_size = queryset.plan.end_size if queryset and queryset.plan and queryset.plan.end_size else 0
    #         file_size = 0 if file_size is None else file_size
    #         if file_size > gb_to_bytes(plan_size):
    #             return response.BadRequest({'detail': 'Your Court storage is full, please contact your admin!'})
    #     file_type = req_data["file_type"] if "file_type" in req_data else None
    #     file_name = req_data["file"] if "file" in req_data else ""
    #     file_name = file_name.split('/')[-1]
    #     file_name = str(randint(100000, 999999)) + "_" + file_name
    #     object_path = 'temp/' + file_name
    #     if file_type and "file" in req_data:
    #         return response.Ok({"url": create_presigned_url(object_path, file_type), "file_name": file_name})
    #     return response.BadRequest({'detail': 'Please provide name of the file'})
    #
    # @action(methods=['POST'], detail=False)
    # def onboard_presigned_url(self, request):
    #     req_data = request.data.copy()
    #     file_type = req_data["file_type"] if "file_type" in req_data else None
    #     file_name = req_data["file"] if "file" in req_data else ""
    #     file_name = file_name.split('/')[-1]
    #     file_name = str(randint(100000, 999999)) + "_" + file_name
    #     object_path = 'temp/' + file_name
    #     if file_type and "file" in req_data:
    #         return response.Ok({"url": create_presigned_url(object_path, file_type), "file_name": file_name})
    #     return response.BadRequest({'detail': 'Please provide name of the file'})
    #
    # @action(methods=['GET'], detail=False)
    # def download_file(self, request):
    #     Court = get_current_Court(request)
    #     path = request.query_params.get('path', None)
    #     is_onboard = request.query_params.get('is_onboard', False)
    #     from ..employee.models import Files
    #     if Court:
    #         file_obj = Files.objects.filter(Court=Court, file_name=path, is_active=True).first()
    #     else:
    #         file_obj = Files.objects.filter(file_name=path, is_active=True).first()
    #     if not path:
    #         response.BadRequest({'detail': 'Please provide the path of the file!'})
    #     return response.Ok({"url": get_presigned_url(object_name=file_obj.file_path if file_obj else path,
    #                                                  is_onboard=is_onboard)})


class DynamicSettingsViewSet(ModelViewSet):
    serializer_class = DynamicSettingsSerializer
    queryset = DynamicSettings.objects.all()
    permission_classes = (DynamicSettingsPermissions,)
    parser_classes = (JSONParser, MultiPartParser)
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = None

    def get_queryset(self):
        queryset = super(DynamicSettingsViewSet, self).get_queryset()
        queryset = queryset.filter(is_active=True)
        self.filterset_class = DynamicSettingsFilter
        queryset = self.filter_queryset(queryset)
        return queryset

    @swagger_auto_schema(
        method="get",
        operation_summary='List of dynamic settings',
        operation_description='Admin can get list of all dynamic settings',
        response=DynamicSettingsSerializer
    )
    @action(methods=['GET'], detail=False)
    def dropdown(self, request):
        dropdown_list = SETTINGS_CONSTANT
        data = dropdown_tree(dropdown_list, DynamicSettingsSerializer, DynamicSettings)
        return response.Ok(data)

    @swagger_auto_schema(
        method="put",
        operation_summary='Update User Storage.',
        operation_description='.',
        request_body=UserSerializer,
        response=UserSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of user storage',
        operation_description='',
        response=UserSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False)
    def users(self, request):
        if request.method == "GET":
            queryset = get_user_model().objects.filter(is_active=True)
            self.filterset_class = UserBasicFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(UserSerializer(page, many=True).data)
            return response.Ok(UserSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, UserSerializer, get_user_model()))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Country',
        operation_description='Add Country',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Country.',
        operation_description='.',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Country',
        operation_description='',
        response=CountrySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Country, filterset_class=CountryFilter)
    def country(self, request):
        if request.method == "GET":
            queryset = Country.objects.filter(is_active=True)
            self.filterset_class = CountryFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CountrySerializer(page, many=True).data)
            return response.Ok(CountrySerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CountrySerializer, Country))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add State',
        operation_description='Add State',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update State.',
        operation_description='.',
        request_body=CountrySerializer,
        response=CountrySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of State',
        operation_description='',
        response=CountrySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=State, filterset_class=StateFilter)
    def state(self, request):
        if request.method == "GET":
            queryset = State.objects.filter(is_active=True)
            self.filterset_class = StateFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(StateSerializer(page, many=True).data)
            return response.Ok(StateSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, StateSerializer, State))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add City',
        operation_description='Add City',
        request_body=CitySerializer,
        response=CitySerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update City.',
        operation_description='.',
        request_body=CitySerializer,
        response=CitySerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of City',
        operation_description='',
        response=CitySerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=City, filterset_class=CityFilter)
    def city(self, request):
        if request.method == "GET":
            queryset = City.objects.filter(is_active=True)
            self.filterset_class = CityFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CitySerializer(page, many=True).data)
            return response.Ok(CitySerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CitySerializer, City))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Court.',
        operation_description='Add Court.',
        request_body=CourtSerializer,
        response=CourtSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Court.',
        operation_description='.',
        request_body=CourtSerializer,
        response=CourtSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Court',
        operation_description='',
        response=CourtSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Court,
            filterset_class=CourtFilter)
    def court(self, request):
        if request.method == "GET":
            queryset = Court.objects.filter(is_active=True)
            self.filterset_class = CourtFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CourtDataSerializer(page, many=True).data)
            return response.Ok(CourtDataSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, CourtSerializer, Court))

    @swagger_auto_schema(
        method="put",
        operation_summary='Update Court.',
        operation_description='.',
        request_body=CourtSerializer,
        response=CourtSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Deleted Court',
        operation_description='',
        response=CourtSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=Court,
            filterset_class=CourtFilter)
    def deleted_court(self, request):
        if request.method == "GET":
            queryset = Court.objects.filter(is_active=False)
            self.filterset_class = CourtFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CourtDataSerializer(page, many=True).data)
            return response.Ok(CourtDataSerializer(queryset, many=True).data)
        else:
            Court_id = request.data.get('id', None)
            if not Court_id:
                return response.BadRequest({'detail': 'Court is required!'})
            Court.objects.filter(id=Court_id).update(is_active=True)
            return response.Ok({'detail': 'Court deletion has been successfully reverted!'})

    @swagger_auto_schema(
        method="get",
        operation_summary='List of Court',
        operation_description='',
        response=CourtSerializer
    )
    @action(methods=['GET'], detail=False, queryset=Court,
            filterset_class=CourtFilter)
    def court_list(self, request):
        if request.method == "GET":
            queryset = Court.objects.filter(is_active=True)
            self.filterset_class = CourtFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(CourtBasicDataSerializer(page, many=True).data)
            return response.Ok(CourtBasicDataSerializer(queryset, many=True).data)

    @swagger_auto_schema(
        method="get",
        operation_summary='List of All Services',
        operation_description='',
        response=DynamicSettingsSerializer
    )
    @action(methods=['GET'], detail=False, queryset=DynamicSettings, filterset_class=DynamicSettingsFilter)
    def all_services(self, request):
        queryset = DynamicSettings.objects.filter(is_active=True)
        self.filterset_class = DynamicSettingsFilter
        queryset = self.filter_queryset(queryset)
        queryset = queryset.filter(name=CORE_SERVICES) | queryset.filter(name=NON_CORE_SERVICES)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(DynamicSettingsSerializer(page, many=True).data)
        return response.Ok(DynamicSettingsSerializer(queryset, many=True).data)

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Employee.',
        operation_description='Add Employee.',
        request_body=EmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Employee.',
        operation_description='.',
        request_body=EmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Employee',
        operation_description='',
        response=EmployeeSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False, queryset=Employee,
            filterset_class=EmployeeFilter)
    def employee(self, request):
        if request.method == "GET":
            queryset = Employee.objects.filter(court__is_active=True, is_active=True)
            self.filterset_class = EmployeeFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(EmployeeSerializer(page, many=True).data)
            return response.Ok(EmployeeSerializer(queryset, many=True).data)
        else:
            request_data = request.data.copy()
            id = request_data.get("id", None)
            email = request_data.get("email", None)
            mobile = request_data.get("mobile", None)
            first_name = request_data.get("first_name", None)
            court = request_data.get("court", None)
            if not court:
                return response.BadRequest({"detail": "Court is required!"})
            if not id:
                if not email:
                    return response.BadRequest({"detail": "Email is required!"})
            user = get_user_model().objects.filter(email=email, is_active=True).first()
            if not user:
                user, password = create_new_user(email=email, mobile=mobile, first_name=first_name)
                template = "employee_added.html"
                subject = "Your profile is added to a new Court"
                data = {
                    'data': UserSerializer(user).data,
                    'login_link': config('employee_DOMAIN')
                }
                if password:
                    subject = "Your profile has been created on CA Cloud Desk."
                    template = "user_created.html"
                    data['password'] = password
                    data['professional_name'] = user.first_name if user.first_name else '--'
                    data['mobile'] = user.mobile if user.mobile else '--'
                    court_obj = Court.objects.filter(id=court, is_active=True).first()
                    data['firm_name'] = court_obj.name if court_obj else '--'
                    send_from_template(user.email, subject, template, data)
                elif not id:
                    send_from_template(user.email, subject, template, data)
                    if user.mobile:
                        name = user.first_name if user.first_name else "User"
            request_data['user'] = user.pk
            return response.Ok(create_update_record(request_data, EmployeeSerializer, Employee))

    @swagger_auto_schema(
        method="put",
        operation_summary='For disabling and deleting employee',
        operation_description='',
        request_body=DeleteEmployeeSerializer,
        response=EmployeeSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of Deleted EmployeeS',
        operation_description='',
        response=EmployeeSerializer
    )
    @action(methods=['GET', 'PUT'], detail=False, queryset=Employee, filterset_class=EmployeeFilter)
    def deleted_employee(self, request):
        if request.method == 'GET':
            queryset = Employee.objects.filter(is_active=False)
            self.filterset_class = EmployeeFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(EmployeeSerializer(page, many=True).data)
            return response.Ok(EmployeeSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, DeleteEmployeeSerializer, Employee))

    @swagger_auto_schema(
        method="post",
        operation_summary='Add Description template',
        operation_description='Admin can add description templates.',
        request_body=DescriptionTemplateSerializer,
        response=DescriptionTemplateSerializer
    )
    @swagger_auto_schema(
        method="put",
        operation_summary='Update Description template',
        operation_description='Admin can update description templates.',
        request_body=DescriptionTemplateSerializer,
        response=DescriptionTemplateSerializer
    )
    @swagger_auto_schema(
        method="get",
        operation_summary='List of description template',
        operation_description='Admin can get list of all description templates.',
        response=DescriptionTemplateSerializer
    )
    @action(methods=['GET', 'POST', 'PUT'], detail=False)
    def description_template(self, request):
        if request.method == "GET":
            queryset = DescriptionTemplate.objects.filter(is_active=True)
            self.filterset_class = DescriptionTemplateFilter
            queryset = self.filter_queryset(queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                return self.get_paginated_response(DescriptionTemplateSerializer(page, many=True).data)
            return response.Ok(DescriptionTemplateSerializer(queryset, many=True).data)
        else:
            return response.Ok(create_update_record(request, DescriptionTemplateSerializer, DescriptionTemplate))