from ..admin_settings.models import Employee


def get_current_court(request):
    return request.META.get('HTTP_COURT', None)


def get_employee_obj(user, court):
    if court and user:
        employee_obj = Employee.objects.filter(user=user, publisher=publisher, is_active=True).first()
        if employee_obj:
            return employee_obj
        else:
            raise ValueError('Invalid Employee')
    return None
