from .accounts.viewsets import UserViewSet
from .admin_settings.viewsets import DynamicSettingsViewSet, UploadedDocumentViewSet
from .base.api.routers import DynamicRouter
from .customer.viewsets import CustomerViewSet

restricted_router = DynamicRouter()

# user
restricted_router.register(r'users', UserViewSet, basename='v1_auth')
restricted_router.register(r'uploads', UploadedDocumentViewSet, basename='v1_uploads')
restricted_router.register(r'admin_settings', DynamicSettingsViewSet, basename='v1_admin')
restricted_router.register(r'customer', CustomerViewSet, basename='v1_customer')