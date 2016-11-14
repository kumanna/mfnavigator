from django.shortcuts import render
from bakery.views import BuildableDetailView, BuildableListView
from .models import AMC, MutualFund, MutualFundStaticJSON
import os, mfnavigator.settings, abc
import datetime, math

# Create your views here.
class AMCListView(BuildableListView):
    model = AMC
    template_name = 'navigator/amc_list.html'
    build_path = 'amcs.html'

class MFListViewJSON(BuildableDetailView):
    model = AMC
    template_name = 'navigator/mfs.json'

    def __init__(self):
        super(MFListViewJSON, self).__init__()

    def get_url(self, obj):
        return '/%s.json' % obj.amfiid

    def get_build_path(self, obj):
        path = os.path.join(mfnavigator.settings.BUILD_DIR)
        os.path.exists(path) or os.makedirs(path)
        return os.path.join(path, str(obj.amfiid) + '.json')

    def get_context_data(self, **kwargs):
        context = super(MFListViewJSON, self).get_context_data(**kwargs)
        obj = context['object']
        context['mflist'] = obj.mutualfund_set.all()
        return context

class LastYearsStaticJSONView(BuildableDetailView,metaclass=abc.ABCMeta):
    model = MutualFund
    template_name = 'navigator/navjson.json'
    n = 0

    def get_url(self, obj):
        return '/%dy-navs/%s.json' % (self.n, obj.amfisymbol)

    def get_build_path(self, obj):
        path = os.path.join(mfnavigator.settings.BUILD_DIR, '%dy-navs' % self.n)
        os.path.exists(path) or os.makedirs(path)
        return os.path.join(path, obj.amfisymbol + '.json')

    def get_context_data(self, **kwargs):
        context = super(LastYearsStaticJSONView, self).get_context_data(**kwargs)
        obj = context['object']
        today = datetime.date.today()
        last_year = today - datetime.timedelta(days=365*self.n)
        context['navvals'] = obj.mutualfundnav_set.filter(date__range = (str(last_year), str(today))).order_by('date')[::self.n]
        return context

class Last1YearStaticJSONView(LastYearsStaticJSONView):
    n = 1

class Last3YearStaticJSONView(LastYearsStaticJSONView):
    n = 3

class Last5YearStaticJSONView(LastYearsStaticJSONView):
    n = 5

class Last7YearStaticJSONView(LastYearsStaticJSONView):
    n = 7

class Last10YearStaticJSONView(LastYearsStaticJSONView):
    n = 10

class LastYearsViewer(BuildableListView,metaclass=abc.ABCMeta):
    model = MutualFund
    n = 0

    def __init__(self):
        self.template_name = 'navigator/allmf_1y.html'
        self.path = os.path.join(mfnavigator.settings.BUILD_DIR, '%dy-navs' % self.n)
        os.path.exists(self.path) or os.makedirs(self.path)
        self.build_path = os.path.join(self.path, 'index.html')

    def get_url(self, obj):
        return '/%dy-navs/' % self.n

class Last1YearViewer(LastYearsViewer):
    n = 1

class Last3YearViewer(LastYearsViewer):
    n = 3

class Last5YearViewer(LastYearsViewer):
    n = 5

class Last7YearViewer(LastYearsViewer):
    n = 7

class Last10YearViewer(LastYearsViewer):
    n = 10

class TopMFViewer(BuildableListView,metaclass=abc.ABCMeta):
    model = MutualFund
    n = 0

    def __init__(self):
        self.template_name = 'navigator/topmfs.html'
        self.path = os.path.join(mfnavigator.settings.BUILD_DIR)
        os.path.exists(self.path) or os.makedirs(self.path)
        self.build_path = os.path.join(self.path, 'topmfs-%d.html' % self.n)

    def get_url(self, obj):
        return '/topmfs-%d.html' % self.n

    def get_context_data(self, **kwargs):
        context = super(TopMFViewer, self).get_context_data(**kwargs)
        today = datetime.date.today()
        last_year = today - datetime.timedelta(days=366*self.n)
        context['mfs'] = []
        for mf in context['object_list']:
            navs = mf.mutualfundnav_set.filter(date__range = (str(last_year), str(today))).order_by('date')
            if len(navs) < 1: continue
            timegap = abs(navs[0].date - navs.last().date)
            # We ensure that the last NAV is close to the number of years from today
            if timegap.days > 365 * self.n - 8:
                absolute_return = float(navs.last().nav / navs[0].nav)
                n_years = float(timegap.days) / 365.00
                compunded_return = math.exp(math.log(absolute_return) / n_years) - 1.0
                context['mfs'].append({'mfname' : mf.mfname, 'value' : compunded_return * 100})
        if len(context['mfs']) > 10:
            context['mfs'] = sorted(context['mfs'], key=lambda x : x['value'], reverse=True)[:20]
        context['year_str'] = '1 year' if self.n == 1 else ("%d years" % self.n)
        return context

class TopMF1YearViewer(TopMFViewer):
    n = 1

class TopMF3YearViewer(TopMFViewer):
    n = 3

class TopMF5YearViewer(TopMFViewer):
    n = 5

class TopMF7YearViewer(TopMFViewer):
    n = 7
