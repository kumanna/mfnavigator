from django.shortcuts import render
from bakery.views import BuildableDetailView, BuildableListView
from .models import AMC, MutualFund, MutualFundStaticJSON
import os, mfnavigator.settings

# Create your views here.
class AMCListView(BuildableListView):
	model = AMC
	template_name = 'navigator/amc_list.html'
	build_path = 'amcs.html'

class MutualFundStaticJSONView(BuildableDetailView):
	model = MutualFund
	template_name = 'navigator/navjson.json'

	def get_url(self, obj):
		return '/%s.json' % obj.amfisymbol

	def get_build_path(self, obj):
		return os.path.join(mfnavigator.settings.BUILD_DIR, obj.amfisymbol + ".json")
