from django.core.management.base import BaseCommand, CommandError
from navigator.models import AMC, MutualFund, MutualFundNAV
import urllib.request
import datetime, time
import decimal

class Command(BaseCommand):
	help = 'Import NAVs from an AMFI style file'
	URL = "http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf={0}&tp=1&frmdt={1}&todt={2}"

	def add_arguments(self, parser):
		parser.add_argument('--amcid', nargs=1, type=int)

	def handle(self, *args, **options):
		AMCID = options['amcid'][0]
		mfs = AMC.objects.filter(amfiid=AMCID)[0]

		# Find the oldest _latest_ NAV date
		today = datetime.date.today()
		mindate = today
		minmf = None
		for mf in mfs.mutualfund_set.all():
			latest_date = mf.mutualfundnav_set.order_by('-date')[0].date
			if latest_date < mindate:
				mindate = latest_date
				minmf = mf.mfname

		# Then create the URL and download and save the
		# required NAVs
		mindate = datetime.date.strftime(mindate, "%d-%h-%Y")
		print("Oldest NAV: {0}, {1}".format(minmf, mindate))
		print("Getting NAVs from %s." % mindate)
		today = datetime.date.strftime(today, "%d-%h-%Y")
		navurl = self.URL.format(AMCID, mindate, today)
		mflist = [i.amfisymbol for i in mfs.mutualfund_set.all()]
		u = urllib.request.urlopen(navurl)
		line = str(u.readline().decode(encoding='ascii'))
		while line:
			field_list = line.split(';')
			if len(field_list) > 3:
				if field_list[0] in mflist:
					m = MutualFund.objects.get(amfisymbol=field_list[0])
					print('%s: %s, %s' % (m.mfname, field_list[3], field_list[-1].strip()))
					t = time.strptime(field_list[-1].strip(), '%d-%b-%Y')
					entry = m.mutualfundnav_set.get_or_create(nav=decimal.Decimal(field_list[3]),
															  date=datetime.date.fromtimestamp(time.mktime(t)))[0]
					entry.save()
			line = u.readline().decode(encoding='ascii')
		u.close()
