from django.shortcuts import render
from bakery.views import BuildableListView
from .models import AMC, MutualFund

# Create your views here.
class AMCListView(BuildableListView):
	model = AMC
	template_name = 'navigator/amc_list.html'
	build_path = 'amcs.html'
