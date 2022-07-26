from django.urls import path,include
from . import views
from rest_framework import routers

router=routers.DefaultRouter()
router.register('database_connections',views.DatabaseConnectionViewSet,basename='database_connection')
router.register('data_models',views.DataModelViewSet,basename='data_model')
router.register('data_source',views.DataSourceViewSet,basename='data_source')
router.register('explorer',views.ExplorerViewSet,basename='explorer')
router.register('register',views.Users,basename='register')

urlpatterns = [
    path('api/',include(router.urls)),
    path('api/login/',views.LoginView.as_view(),name="login_view"),
    # path('api_login',include('rest_framework.urls',namespace="api_login")),
    path('api/send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('api/reset-password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='reset-password'),
]





