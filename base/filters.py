import django_filters
from django_filters import CharFilter

from django import forms

from .models import *
class PostFilterName(django_filters.FilterSet):
	headline = CharFilter(field_name='headline', lookup_expr="icontains", label=' ')

	class Meta:
		model = Post
		fields = ['headline']

class PostFilter(django_filters.FilterSet):
	headline = CharFilter(field_name='headline', lookup_expr="icontains", label='Пошук за назвою')
	tags = django_filters.ModelChoiceFilter(queryset=Tag.objects.all(),  label='Пошук за категорією')


	class Meta:
		model = Post
		fields = ['headline', 'tags']


