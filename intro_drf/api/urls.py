from .views import InstitutionsView, MetadataView, ReportsView
from django.urls import path, include

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-metadata',MetadataView.as_view() , name='get-metadata'),
    path('get-reports', ReportsView.as_view() , name='get-reports'),
]
