from django.contrib import admin

from .models import AMC, MutualFund, MutualFundNAV

admin.site.register(AMC)
admin.site.register(MutualFund)
admin.site.register(MutualFundNAV)
