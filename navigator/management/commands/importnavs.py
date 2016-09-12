from django.core.management.base import BaseCommand, CommandError
from navigator.models import AMC, MutualFund, MutualFundNAV
import datetime, time
import decimal

class Command(BaseCommand):
	help = 'Import NAVs from an AMFI style file'

	def add_arguments(self, parser):
		parser.add_argument('--amcid', nargs=1, type=int)
		parser.add_argument('--amfinumber', nargs=1, type=str)
		parser.add_argument('--mfname', nargs=1, type=str)
		parser.add_argument('--navfile', nargs=1, type=str)

	def handle(self, *args, **options):
		AMCID = options['amcid'][0]
		AMFINUMBER = options['amfinumber'][0]
		MFNAME = options['mfname'][0]
		MFNAME = MFNAME.replace('"', '')
		NAVFILE = options['navfile'][0]

		with open(NAVFILE, 'r') as f:
			lines = f.readlines()

		# Keep only the required lines
		lines = [i for i in lines if i.startswith(AMFINUMBER)]
		m = MutualFund.objects.get_or_create(amfisymbol=AMFINUMBER,
											 mfname=MFNAME,
											 amfiid=AMC.objects.get(amfiid=AMCID))[0]
		for navline in lines:
			field_list = navline.split(';')
			print('%s, %s' % (field_list[3], field_list[-1].strip()))
			t = time.strptime(field_list[-1].strip(), '%d-%b-%Y')
			entry = m.mutualfundnav_set.get_or_create(nav=decimal.Decimal(field_list[3]),
													  date=datetime.date.fromtimestamp(time.mktime(t)))[0]
			entry.save()
		m.save()
