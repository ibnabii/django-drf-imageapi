from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from imageapi.models import Profile, ServicePlan, PlanThumbnail


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ThumbsInline(admin.TabularInline):
    model = PlanThumbnail
    verbose_name_plural = 'Thumbnail sizes'
    verbose_name = 'Thumbnail size'
    extra = 0


class SerivcePlanAdmin(admin.ModelAdmin):
    inlines = (ThumbsInline,)


admin.site.register(ServicePlan, SerivcePlanAdmin)

