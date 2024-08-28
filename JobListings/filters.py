from .models import JobModel
from django_filters import rest_framework as filters

class JobFilters(filters.FilterSet):
    min_salary=filters.NumberFilter(field_name='salary_range',lookup_expr='gte')
    max_salary=filters.NumberFilter(field_name='salary_range',lookup_expr='lte')
    location=filters.CharFilter(field_name='location',lookup_expr='icontains')
    employment_type=filters.ChoiceFilter(field_name='employment_type',choices=JobModel.employment_type_choices)
    title=filters.CharFilter(field_name='title',lookup_expr='icontains')
    
    class Meta:
        model=JobModel
        fields=['min_salary','max_salary','location','employment_type','title']
    