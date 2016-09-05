from django.db import models

class AMC(models.Model):
    amfiid = models.IntegerField(unique=True)
    amcname = models.CharField(max_length=100,default='Unnamed AMC')

    def __str__(self):
        return str(self.amfiid)

class MutualFund(models.Model):
    """
    Basic mutual fund. We store the AMFI number as well as the six
    digit AMFI symbol number currently.
    """
    amfisymbol = models.CharField(max_length=10, unique=True)
    mfname = models.CharField(max_length=300,default='Unnamed MF')
    amfiid = models.ForeignKey(AMC)

    def __str__(self):
        return self.mfname + ' (' + self.amfisymbol + ')'

class MutualFundNAV(models.Model):
    """Class to store each NAV entry."""
    mf = models.ForeignKey(MutualFund, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    nav = models.DecimalField(max_digits=20,decimal_places=6)

    def __str__(self):
        return "%s, %s, %s" % (self.mf.amfisymbol, str(self.date), str(self.nav))
