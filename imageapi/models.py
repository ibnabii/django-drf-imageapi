from datetime import datetime, timedelta
from uuid import uuid4
from re import search

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image as Pilimg

def random_filename(filename=''):
    extension = search(r'.*(\..*)$', filename)
    if (extension):
        extension = extension.group(1)
    else:
        extension = ''
    return f'{uuid4().hex}{extension}'

def random_path(instance, filename):
    extension = search(r'.*(\..*)$', filename)
    if (extension):
        extension = extension.group(1)
    print(extension, filename)
    return settings.MEDIA_ROOT / f'{uuid4().hex}{extension}'


def png_or_jpg(value):
    image = Pilimg.open(value)
    if image.format not in ['JPEG', 'PNG']:
        raise ValidationError('File is neither of jpeg nor png type')

def longevity_validator(value):
    MIN_SECONDS = 30
    MAX_SECONDS = 30000
    if MIN_SECONDS <= value <= MAX_SECONDS:
        return
    raise ValidationError(f'Allowed life time of temp link is between {MIN_SECONDS} and {MAX_SECONDS} seconds.')


class ServicePlan(models.Model):
    name = models.CharField('Plan name', max_length=20, blank=False, null=False)
    canLinkOrig = models.BooleanField('Is linking the original image allowed in this plan?', default=False)
    canCreateTempLink = models.BooleanField('Can user create an expiring link to the image?', default=False)

    def __str__(self):
        return self.name


class PlanThumbnail(models.Model):
    height = models.IntegerField('Height in pixels', blank=False, null=False)
    plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE, related_name='thumbs')

    def __str__(self):
        return f'{self.plan.name}: {self.height}px'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True)


class Image(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    img = models.ImageField(upload_to=random_path, validators=[png_or_jpg])
    owner = models.ForeignKey('auth.User', related_name='images', on_delete=models.CASCADE)
    temp_link = models.URLField(max_length=200, blank=True, null=True)
    temp_id = models.SlugField(max_length=200, blank=True, null=True)
    temp_link_expire_time = models.DateTimeField(null=True)
    temp_link_longevity = models.IntegerField(blank=True, validators=[longevity_validator], null=True)


class ImageThumbnail(models.Model):
    original = models.ForeignKey(Image, related_name='thumbnails', on_delete=models.CASCADE)
    size = models.ForeignKey(PlanThumbnail, related_name='images', on_delete=models.CASCADE)
    img = models.ImageField()

