from django.urls import path

from api.base.v1.views.actionView import ActionView
from api.base.v1.views.checkUserView import CheckUserNameView, CheckEmailView
from api.base.v1.views.loginView import LoginView
from api.base.v1.views.permissionView import PermissionView
from api.base.v1.views.registerView import RegisterView
from api.base.v1.views.reportDataView import ReportDataView
from api.base.v1.views.sensorDataView import SensorDataView
from api.base.v1.views.userView import UserView
from api.base.v1.views.adminMapView import AdminMapView

urlpatterns = [
    path('v1/user/', UserView.as_view(), name='Get user list'),
    path('v1/permission/', PermissionView.as_view(), name='Get permission list'),
    path('v1/login/', LoginView.as_view(), name='Login'),
    path('v1/register/', RegisterView.as_view(), name='Register'),
    path('v1/checkusername/', CheckUserNameView.as_view(), name='check user name'),
    path('v1/checkemail/', CheckEmailView.as_view(), name='check email'),
    path('v1/dashboard/', SensorDataView.as_view(), name='get sensors data'),
    path('v1/action/', ActionView.as_view(), name='get sensors data'),
    path('v1/admin_map/', AdminMapView.as_view(), name='get sensors data'),
    path('v1/report_data/', ReportDataView.as_view(), name='get sensors data'),

]
