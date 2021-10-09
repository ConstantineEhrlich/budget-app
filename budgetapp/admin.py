from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Income)
admin.site.register(Outcome)
admin.site.register(Budget_Line)
admin.site.register(UserBudget)