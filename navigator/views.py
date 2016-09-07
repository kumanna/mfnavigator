from django.shortcuts import render
from bakery.views import BuildableDetailView, BuildableListView
from .models import AMC, MutualFund, MutualFundStaticJSON
import os, mfnavigator.settings
import datetime

# Create your views here.
class AMCListView(BuildableListView):
	model = AMC
	template_name = 'navigator/amc_list.html'
	build_path = 'amcs.html'

class LastYearStaticJSONView(BuildableDetailView):
	model = MutualFund
	template_name = 'navigator/navjson.json'

	def get_url(self, obj):
		return '/1y-navs/%s.json' % obj.amfisymbol

	def get_build_path(self, obj):
		path = os.path.join(mfnavigator.settings.BUILD_DIR, '1y-navs')
		os.path.exists(path) or os.makedirs(path)
		return os.path.join(path, obj.amfisymbol + '.json')

	def get_context_data(self, **kwargs):
		context = super(LastYearStaticJSONView, self).get_context_data(**kwargs)
		obj = context['object']
		today = datetime.date.today()
		last_year = today - datetime.timedelta(days=365)
		context['navvals'] = obj.mutualfundnav_set.filter(date__range = (str(last_year), str(today))).order_by('date')
		return context
