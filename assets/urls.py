from django.urls import path
from .views import DashboardView, AssetListView, AssetCreateView, SignUpView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', AssetListView.as_view(), name='asset-list'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('register/', SignUpView.as_view(), name='register'),
]