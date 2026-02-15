from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, DecimalField, Value
from django.db.models.functions import Coalesce
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django import forms
from django.forms import ModelForm

from .forms import CustomCreationForm, CustomAuthenticationForm
from .models import Asset, Department, MaintenanceLog
from .mixins import ManagerRequiredMixin

class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ["name", "asset_type", "cost", "assigned_to"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "asset_type": forms.Select(attrs={"class": "form-select"}),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
        }

class MaintenanceForm(ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ["description", "cost", "date_repaired"]
        widgets = {
            "description": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter description"
            }),
            "cost": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter cost"
            }),
            "date_repaired": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

class AssetCreateView(ManagerRequiredMixin, CreateView):
    model = Asset
    form_class = AssetForm
    template_name = "assets/asset_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Asset created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to create asset. Please check inputs.")
        return super().form_invalid(form)
    
class AssetDeleteView(ManagerRequiredMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy("dashboard")  # or "asset-list"

    def form_valid(self, form):
        messages.success(self.request, "Asset deleted successfully.")
        return super().form_valid(form)

# TOPIC 5: Class-Based Views (CBVs) & TOPIC 4: Aggregation
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "assets/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Aggregation: Calculate total value of all assets
        total_cost = Asset.objects.aggregate(total=Sum("cost"))["total"] or 0
        context["total_asset_value"] = total_cost

        # Annotation/Count: Assets per type
        context["assets_by_type"] = (
            Asset.objects.values("asset_type")
            .annotate(count=Count("id"))
            .order_by("asset_type")
        )

        # Aggregation: Total cost of assets by department
        context["cost_by_department"] = (
            Department.objects.annotate(
                total_cost=Coalesce(
                    Sum("users__assets__cost"),
                    Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .values("name", "total_cost")
            .order_by("name")
        )

        context["assets"] = (
            Asset.objects.select_related("assigned_to")
            .annotate(
                repair_total=Coalesce(
                    Sum("maintenance_logs__cost"),
                    Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .order_by("-created_at")
        )

        context["asset_form"] = AssetForm()

        context["maintenance_form"] = MaintenanceForm()

        return context


# TOPIC 3: Optimize SQL Queries
class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets/asset_list.html"
    context_object_name = "assets"

    def get_queryset(self):
        # Optimization: Use select_related to fetch the 'assigned_to' User
        # in the same query, preventing the N+1 problem.
        return (
            Asset.objects.select_related("assigned_to")
            .annotate(
                repair_total=Coalesce(
                    Sum("maintenance_logs__cost"),
                    Value(0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )
            .all()
        )

class MaintenanceCreateView(ManagerRequiredMixin, CreateView):
    model = MaintenanceLog
    template_name = "assets/maintenance_form.html"
    fields = ["description", "cost", "date_repaired"]
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        self.asset = get_object_or_404(Asset, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.asset = self.asset

        messages.success(
            self.request,
            f"Repair log saved for '{self.asset.name}'."
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Failed to save repair log. Please check the inputs."
        )
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["asset"] = self.asset
        return context


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, "You have logged in successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)
    
class CustomLogoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "Logged out successfully.")
        return redirect("login")
    
class SignUpView(CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"

    def form_valid(self, form):
        messages.success(self.request, "Your account has been created successfully.")
        return super().form_valid(form)