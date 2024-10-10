from ..base.api.permissions import (AllowAny, IsAuthenticated, PermissionComponent, ResourcePermission, IsSuperUser,
                                    AllOnlyGetPerm, AllowAnyGetPerm, AllowAnyPostPerm)


class IsTheSameUser(PermissionComponent):
    def has_permission(self, request, view):
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj=None):
        return request.user.is_authenticated() and request.user.pk == obj.pk


class DynamicSettingsPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = IsSuperUser() | IsAuthenticated()
    create_perms = IsSuperUser()
    update_perms = IsSuperUser()
    partial_update_perms = IsSuperUser()
    destroy_perms = IsSuperUser()
    list_perms = IsSuperUser() | IsAuthenticated() | AllOnlyGetPerm()
    dropdown_perms = IsSuperUser() | AllOnlyGetPerm()
    users_perms = IsSuperUser()
    country_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    state_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    city_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    gst_setting_perms = IsSuperUser() | AllOnlyGetPerm()
    sms_setting_perms = IsSuperUser() | AllOnlyGetPerm()
    subscription_plan_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    policies_perms = IsSuperUser() | AllOnlyGetPerm() | AllowAnyGetPerm()
    employee_policies_perms = IsSuperUser()
    court_perms = IsSuperUser()
    all_services_perms = IsSuperUser()
    deleted_court_perms = IsSuperUser()
    court_list_perms = IsSuperUser()
    employee_perms = IsSuperUser()
    deleted_employee_perms = IsSuperUser()
    credits_perms = IsSuperUser() | AllOnlyGetPerm()
    current_credits_perms = IsSuperUser() | AllOnlyGetPerm()
    employee_kyc_perms = IsSuperUser()
    coupon_code_perms = IsSuperUser()
    hsn_settings_perms = IsSuperUser() | AllOnlyGetPerm()
    send_coupon_perms = IsSuperUser()
    description_template_perms = IsSuperUser()
    faq_template_perms = IsSuperUser()
    faq_bulk_perms = IsSuperUser()
    self_document_perms = IsSuperUser() | AllOnlyGetPerm()
    subscription_perms = IsSuperUser()
    version_perms = AllowAny()
    lead_perms = IsSuperUser() | AllowAnyPostPerm()
    on_boarding_perms = IsSuperUser() | AllowAnyPostPerm()
    on_boarding_approve_perms = IsSuperUser()
    request_onbording_perms = AllowAnyPostPerm()
    onbording_status_perms = AllowAny()
    onboard_coupon_code_perms = IsSuperUser()
    check_onboard_coupon_perms = AllowAny()
    check_onboard_tax_perms = AllowAny()
    demo_meeting_perms = IsSuperUser() | AllowAnyPostPerm()
    ticket_approval_perms = IsSuperUser()
    reports_perms = IsSuperUser()
    case_perms = IsSuperUser()
    customer_perms = IsSuperUser()


class UploadedDocumentPermissions(ResourcePermission):
    metadata_perms = AllowAny()
    enough_perms = None
    global_perms = None
    retrieve_perms = AllowAny()
    create_perms = AllowAny()
    update_perms = IsSuperUser()
    partial_update_perms = IsSuperUser()
    destroy_perms = IsSuperUser()
    list_perms = AllowAny()
    create_with_base64_perms = AllowAny()
    multiple_perms = AllowAny()
    presigned_url_perms = AllowAny()
    onboard_presigned_url_perms = AllowAny()
    download_file_perms = AllowAny()
