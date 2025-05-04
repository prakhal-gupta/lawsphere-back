import django_filters
from .models import Customer, Case

class CustomerFilter(django_filters.FilterSet):

    class Meta:
        model = Customer
        fields = {
            'user': ['exact'],
            'id': ['exact'],
            'name': ['exact', 'icontains'],
            'mobile': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'aadhar_no': ['exact', 'icontains'],
            'pan_no': ['exact', 'icontains'],
            'father_name': ['exact', 'icontains'],
            'state': ['exact'],
            'city': ['exact'],
            'address': ['exact', 'icontains'],
            'pincode': ['exact', 'icontains'],
            'is_aadhar_verified': ['exact'],
            'is_active': ['exact'],
        }

class CaseFilter(django_filters.FilterSet):

    class Meta:
        model = Case
        fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'prosecutor_lawyer': ['exact', 'icontains'],
            'defender_lawyer': ['exact', 'icontains'],
            'accused_name': ['exact', 'icontains'],
            'victim_name': ['exact', 'icontains'],
            'status': ['exact', 'icontains'],
            'priority': ['exact'],
            'case_type': ['exact'],
            'case_subtype': ['exact', 'icontains'],
            'number_of_parties': ['exact', 'lt', 'gt'],
            'seriousness': ['exact', 'icontains'],
            'sections': ['exact', 'icontains'],
            'judgment': ['exact', 'icontains'],
            'filing_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'employee': ['exact'],
            'accused': ['exact'],
            'victim': ['exact'],
            'court': ['exact'],
            'judge': ['exact'],
            'user': ['exact'],
            'next_hearing_time': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'previous_hearing_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'next_hearing_date': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'created_at': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'is_active': ['exact'],
        }
