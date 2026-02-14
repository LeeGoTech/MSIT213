from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, F, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomCreationForm

from .models import Asset
from .mixins import ManagerRequiredMixin

# TOPIC 5: Class-Based Views (CBVs) & TOPIC 4: Aggregation
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "assets/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aggregation: Calculate total value of all assets
        total_cost = Asset.objects.aggregate(total=Sum('cost'))['total'] or 0
        context['total_asset_value'] = total_cost

        # Annotation/Count: Assets per type
        context['assets_by_type'] = Asset.objects.values('asset_type').annotate(count=Count('id'))
        
        return context

# TOPIC 3: Optimize SQL Queries
class AssetListView(LoginRequiredMixin, ListView):
    model = Asset
    template_name = "assets/asset_list.html"
    context_object_name = "assets"

    def get_queryset(self):
        # Optimization: Use select_related to fetch the 'assigned_to' User 
        # in the same query, preventing the N+1 problem.
        return Asset.objects.select_related('assigned_to').all()
    
class AssetCreateView(ManagerRequiredMixin, CreateView):
    model = Asset
    template_name = "assets/asset_form.html"
    fields = ['name', 'asset_type', 'cost', 'assigned_to']
    success_url = reverse_lazy('asset-list')

    def form_valid(self, form):
        print(f"Creating asset: {form.instance.name}")
        return super().form_valid(form)

class SignUpView(CreateView):
    form_class = CustomCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'