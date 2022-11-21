from uuid import uuid4
from re import search

from django.conf import settings
from PIL import Image as PILImage

from imageapi.models import Image, ImageThumbnail


def random_filename(filename=''):
    extension = search(r'.*(\..*)$', filename)
    if (extension):
        extension = extension.group(1)
    else:
        extension = ''
    return f'{uuid4().hex}{extension}'


def re_render_thumbnails(queryset):
    """
    Given Image objects will have their thumbnails re-rendered per current service plan
    of their owner. Should be run:
    - when a new image is created - to create thumbnails for the first time
    - when user changes service plan - to adapt available thumbnails to his current setup
    - when service plan is modified by adding, removing or changing thumbs size
    :param queryset: Image objects, for which thumbnails are to be re-rendered
    :return: count of images, for which thumbnails were re-rendered
    """
    if queryset.count():
        for item in queryset:
            # delete existing thumbnails
            # note that deleting related files is handled by catching pre_delete signal
            # this actually happens for both Image and ImageThumbnail, see signals.py
            try:
                for thumb in item.thumbnails.all():
                    thumb.delete()
            except (ImageThumbnail.DoesNotExist, FileNotFoundError):
                continue

            # traverse: image -> owner -> profofile -> service plan -> PlanThumbnail
            for thumb in item.owner.profile.plan.thumbs.all():
                try:
                    thumb_image = PILImage.open(item.img)
                except FileNotFoundError:
                    break
                else:
                    thumb_image.thumbnail([thumb.height * 5, thumb.height])
                    thumb_path = random_filename(item.img.path)
                    thumb_image.save(settings.MEDIA_ROOT / thumb_path)

                    new_thumbnail = ImageThumbnail(
                        original=item,
                        size=thumb,
                        img=str(thumb_path)
                    )
                    new_thumbnail.save()
    return queryset.count()

