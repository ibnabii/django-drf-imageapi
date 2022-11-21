from datetime import datetime, timedelta
import os

from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse


from imageapi.functions import re_render_thumbnails, random_filename
from imageapi.models import Image, ImageThumbnail, Profile, PlanThumbnail


@receiver(pre_delete, sender=Image)
@receiver(pre_delete, sender=ImageThumbnail)
def delete_uploaded_picture(sender, instance, using, **kwargs):
    try:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.img)))
    except:
        pass

@receiver(post_save, sender=Profile)
def update_user_thumbs(sender, instance, created, **kwargs):
    queryset = Image.objects.filter(owner=instance.user)
    re_render_thumbnails(queryset)

@receiver(post_save, sender=PlanThumbnail)
def update_plan_thumbs(sender, instance, created, **kwargs):
    queryset = Image.objects.filter(owner__in=
                                    Profile.objects.filter(plan=instance.plan).values('user')
                                    )
    re_render_thumbnails(queryset)

# @receiver(pre_save, sender=Image)
# def create_temp_link(sender, instance, **kwargs):
#     if instance.temp_link_longevity:
#         instance.temp_link_expire_time = datetime.now() + timedelta(seconds=instance.temp_link_longevity)
#         instance.temp_link = random_filename()
#         instance.temp_link_longevity = 0
