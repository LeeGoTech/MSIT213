from django.urls import path
from .views import DashboardView, AssetCreateView, AssetDeleteView, MaintenanceCreateView, CustomLoginView, CustomLogoutView, SignUpView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('asset/<int:pk>/maintain/', MaintenanceCreateView.as_view(), name='asset-maintain'),
    path("assets/<int:pk>/delete/", AssetDeleteView.as_view(), name="asset-delete"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('register/', SignUpView.as_view(), name='register'),
]
