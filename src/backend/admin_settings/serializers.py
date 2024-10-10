import datetime
import requests
from decouple import config
import google.auth.transport.requests

from django.conf import settings
from django.db.models import Sum, Q, FloatField
from rest_framework import serializers
from django.forms.models import model_to_dict

from .constants import TRANSACTION_SUCCESS, TRANSACTION_PROCESSING, TRANSACTION_FAILED, CORE_SERVICES, PROFESSION
from .models import DynamicSettings, Country, State, City, Court, Employee, UploadedDocument, CsvPdfReports, \
    DescriptionTemplate, EmployeePermissions, Documents, Customer, Case
from .services import delete_child, get_presigned_url, employee_photo_path, create_update_s3_record

from ..accounts.serializers import UserBasicDataSerializer, UserSerializer
from ..accounts.models import User

from ..base.serializers import ModelSerializer
from ..base.services import gb_to_bytes, bytes_to_mb, create_update_record, create_update_manytomany_record
from ..base.utils.email import send_from_template
from ..base.utils.timezone import localtime, now_local


class UploadedDocumentSerializer(ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ('id', 'image_path', 'name', 'image', 'is_active')

    def create(self, validated_data):
        validated_data['is_active'] = True
        doc_image = UploadedDocument.objects.create(**validated_data)
        return doc_image


class DynamicSettingsSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = '__all__'

    def update(self, instance, validated_data):
        is_active = validated_data.get('is_active', True)
        if not is_active:
            delete_child(instance, DynamicSettings)
        DynamicSettings.objects.filter(is_active=True, id=instance.pk).update(**validated_data)
        instance = DynamicSettings.objects.filter(id=instance.pk).first()
        return instance


class DynamicSettingsDataSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = ('id', 'value', 'icon', 'is_active')


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        location = Country.objects.filter(name=name, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "Country already exists."})
        return data


class StateBasicDataSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'state_code', 'is_territorial')


class StateSerializer(ModelSerializer):
    country_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = State
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        location = State.objects.filter(name=name, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "State already exists."})
        return data

    @staticmethod
    def get_country_data(obj):
        return CountrySerializer(obj.country).data if obj.country else None


class CityBasicDataSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'state')


class CitySerializer(ModelSerializer):
    state_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = City
        fields = '__all__'

    def validate(self, data):
        name = data.get('name', None)
        state = data.get('state', None)
        location = City.objects.filter(name=name, state=state, is_active=True)
        if self.instance and self.instance.id:
            location = location.exclude(id=self.instance.id)
        if name and location.exists():
            raise serializers.ValidationError({"detail": "City already exists."})
        return data

    @staticmethod
    def get_state_data(obj):
        return StateSerializer(obj.state).data if obj.state else None


class CountryBasicSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')


class StateBasicSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name',)


class CityBasicSerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)


class DynamicSettingsValueSerializer(ModelSerializer):
    class Meta:
        model = DynamicSettings
        fields = ('value',)


class CourtBasicDataSerializer(ModelSerializer):
    category_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Court
        fields = '__all__'

    @staticmethod
    def get_category_data(obj):
        return DynamicSettingsDataSerializer(obj.category).data if obj.category else None


class CourtDataSerializer(ModelSerializer):
    country_data = serializers.SerializerMethodField(required=False)
    state_data = serializers.SerializerMethodField(required=False)
    city_data = serializers.SerializerMethodField(required=False)
    manager_data = serializers.SerializerMethodField(required=False)
    category_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Court
        fields = '__all__'

    @staticmethod
    def get_country_data(obj):
        return CountrySerializer(obj.country).data if obj.country else None

    @staticmethod
    def get_state_data(obj):
        return StateSerializer(obj.state).data if obj.state else None

    @staticmethod
    def get_city_data(obj):
        return CitySerializer(obj.city).data if obj.city else None

    @staticmethod
    def get_manager_data(obj):
        return UserBasicDataSerializer(obj.manager).data if obj.manager else None

    @staticmethod
    def get_category_data(obj):
        return DynamicSettingsDataSerializer(obj.category).data if obj.category else None


class DocumentsSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class CourtSerializer(ModelSerializer):
    country_data = serializers.SerializerMethodField(required=False)
    state_data = serializers.SerializerMethodField(required=False)
    city_data = serializers.SerializerMethodField(required=False)
    manager_data = serializers.SerializerMethodField(required=False)
    category_data = serializers.SerializerMethodField(required=False)
    documents = DocumentsSerializer(required=False, many=True)

    class Meta:
        model = Court
        fields = '__all__'

    def create(self, validated_data):
        documents = create_update_manytomany_record(validated_data.pop("documents", []), Documents)
        instance = Court.objects.create(**validated_data)
        instance.documents.set(documents)
        instance.save()
        if instance.email:
            template = "user_created.html"
            subject = "Court Created"
            data = {
                'data': {'name': instance.name},
            }
            send_from_template(instance.email, subject, template, data)
        return instance

    def update(self, instance, validated_data):
        documents = create_update_manytomany_record(validated_data.pop("documents", []), Documents, instance.documents)
        Court.objects.filter(id=instance.id).update(**validated_data)
        instance = Court.objects.filter(id=instance.id).first()
        instance.documents.set(documents)
        instance.save()
        return Court.objects.filter(id=instance.id).first()

    @staticmethod
    def get_country_data(obj):
        return CountrySerializer(obj.country).data if obj.country else None

    @staticmethod
    def get_state_data(obj):
        return StateBasicDataSerializer(obj.state).data if obj.state else None

    @staticmethod
    def get_city_data(obj):
        return CityBasicDataSerializer(obj.city).data if obj.city else None

    @staticmethod
    def get_manager_data(obj):
        return UserBasicDataSerializer(obj.manager).data if obj.manager else None

    @staticmethod
    def get_category_data(obj):
        return DynamicSettingsDataSerializer(obj.category).data if obj.category else None


class EmployeePermissionsSerializer(ModelSerializer):
    class Meta:
        model = EmployeePermissions
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    permissions = EmployeePermissionsSerializer(required=False, many=True)
    user_data = serializers.SerializerMethodField(required=False)
    court_data = serializers.SerializerMethodField(required=False)
    designation_data = serializers.SerializerMethodField(required=False)
    department_data = serializers.SerializerMethodField(required=False)
    documents = DocumentsSerializer(required=False, many=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def validate(self, data):
        court = data.get('court', None)
        user = data.get('user', None)
        first_name = data.get('first_name', None)
        queryset = Employee.objects.filter(court=court, is_active=True)
        queryset = queryset.filter(Q(user=user) | Q(first_name=first_name))
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise serializers.ValidationError({"detail": "This user already added with this Court"})
        return data

    def create(self, validated_data):
        court = validated_data.get('court', None)
        path = employee_photo_path(court.id if court else None)
        # file_size, validated_data['photo'] = create_update_s3_record(
        #     to_path=validated_data.get('photo', None), path=path)
        # permission_values = create_update_manytomany_record(validated_data.pop("permissions", []), EmployeePermissions)
        # documents = create_update_manytomany_record(validated_data.pop("documents", []), Documents)
        instance = Employee.objects.create(**validated_data)
        # instance.permissions.set(permission_values)
        # instance.documents.set(documents)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        court = validated_data.get('court', None)
        path = employee_photo_path(court.id if court else None)
        # file_size, validated_data['photo'] = create_update_s3_record(
        #     from_path=instance.photo, to_path=validated_data.get('photo', None), path=path)
        # permission_values = create_update_manytomany_record(validated_data.pop("permissions", []), EmployeePermissions,
        #                                                     instance.permissions)
        # documents = create_update_manytomany_record(validated_data.pop("documents", []), Documents, instance.documents)
        Employee.objects.filter(id=instance.id).update(**validated_data)
        instance = Employee.objects.filter(id=instance.id).first()
        # instance.permissions.set(permission_values)
        # instance.documents.set(documents)
        instance.save()
        return instance

    @staticmethod
    def get_user_data(obj):
        from ..employee.serializers import UserEmployeeSerializer
        return UserEmployeeSerializer(obj.user).data if obj.user else None

    @staticmethod
    def get_court_data(obj):
        return CourtBasicDataSerializer(obj.court).data if obj.court else None

    @staticmethod
    def get_designation_data(obj):
        return DynamicSettingsDataSerializer(obj.designation, many=False).data if obj.designation else None

    @staticmethod
    def get_department_data(obj):
        return DynamicSettingsDataSerializer(obj.department, many=False).data if obj.department else None


class DeleteEmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'is_disabled', 'is_active')


class EmployeeListSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Employee
        fields = '__all__'

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None


class CsvPdfReportSerializer(ModelSerializer):
    report_upload = serializers.SerializerMethodField()

    class Meta:
        model = CsvPdfReports
        fields = '__all__'

    @staticmethod
    def get_report_upload(obj):
        return get_presigned_url(obj.report_upload.name) if obj.report_upload and obj.report_upload.name else None


class DescriptionTemplateSerializer(ModelSerializer):
    service_data = serializers.SerializerMethodField(required=False)
    is_core = serializers.SerializerMethodField(required=False)

    class Meta:
        model = DescriptionTemplate
        fields = '__all__'

    def validate(self, data):
        service = data.get('service', None)
        if not service:
            raise serializers.ValidationError({'detail': 'Service is required!'})
        description_query = DescriptionTemplate.objects.filter(service=service, is_active=True)
        if self.instance:
            description_query = description_query.exclude(id=self.instance.id)
        if description_query.exists():
            raise serializers.ValidationError({'detail': 'Description is already added for this service!'})
        return data

    @staticmethod
    def get_service_data(obj):
        return DynamicSettingsDataSerializer(obj.service, many=False).data if obj.service else None

    @staticmethod
    def get_is_core(obj):
        return obj.service.name == CORE_SERVICES


class CustomerSerializer(ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class CaseSerializer(ModelSerializer):
    user_data = serializers.SerializerMethodField(required=False)
    victim_data = serializers.SerializerMethodField(required=False)
    accused_data = serializers.SerializerMethodField(required=False)
    court_data = serializers.SerializerMethodField(required=False)
    employee_data = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Case
        fields = '__all__'

    @staticmethod
    def get_court_data(obj):
        return CourtBasicDataSerializer(obj.court).data if obj.court else None

    @staticmethod
    def get_victim_data(obj):
        return CustomerSerializer(obj.victim).data if obj.victim else None

    @staticmethod
    def get_accused_data(obj):
        return CustomerSerializer(obj.accused).data if obj.accused else None

    @staticmethod
    def get_employee_data(obj):
        return EmployeeSerializer(obj.employee).data if obj.employee else None

    @staticmethod
    def get_user_data(obj):
        return UserBasicDataSerializer(obj.user).data if obj.user else None
