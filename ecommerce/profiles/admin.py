from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):

    class Meta:
        fields = '__all__'

admin.site.register(Profile, ProfileAdmin)