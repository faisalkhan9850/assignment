from rest_framework import routers
from django.conf.urls import url, include
from rest_api import views
router = routers.DefaultRouter()

router.register(r'signup', views.SignupViewSet, base_name='signup')
router.register(r'employee', views.EmployeeViewSet, base_name='employee')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login', views.LoginView.as_view(), name="login"),
]
