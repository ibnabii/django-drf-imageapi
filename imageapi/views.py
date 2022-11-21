from datetime import datetime, timedelta
import os


from django.views import View
from django.http import FileResponse, Http404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from imageapi.functions import re_render_thumbnails, random_filename
from imageapi.models import Profile, ServicePlan, Image, ImageThumbnail
from imageapi.serializers import ServicePlanSerializer, ImageSerializer, ImageThumbnailSerializer


class ServicePlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to Service Plans definitions.
    """
    queryset = ServicePlan.objects.all().order_by('id')
    serializer_class = ServicePlanSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            # plan = ServicePlan.objects.get(pk=Profile.objects.get(user_id=request.user.id).plan_id)
            plan = request.user.profile.plan
            response.data['current_plan'] = ServicePlanSerializer(plan, context={'request': request}).data
        except (Profile.DoesNotExist, ServicePlan.DoesNotExist):
            response.data['current_plan'] = {}
        return response


class ImageViewSet(viewsets.ModelViewSet):
    """
    Provides actions for image handling
    """
    queryset = Image.objects.all().order_by('-id')
    serializer_class = ImageSerializer

    def generate_temp_link(self, request):
        temp_id = random_filename()
        return {
            'temp_link_expire_time': datetime.now() + timedelta(seconds=int(request.data['temp_link_longevity'])),
            'temp_id': temp_id,
            'temp_link': 'http://' + request.get_host() + reverse('templink', args=[temp_id]),
            'temp_link_longevity': 0
        }

    def perform_create(self, serializer):
        if serializer.context['request'].data.get('temp_link_longevity', None):
            data = self.generate_temp_link(serializer.context['request'])
            obj = serializer.save(owner=self.request.user, **data)
        else:
            obj = serializer.save(owner=self.request.user)
        re_render_thumbnails(Image.objects.filter(id=obj.id))

    def perform_update(self, serializer):
        if serializer.context['request'].data.get('temp_link_longevity', None):
            data = self.generate_temp_link(serializer.context['request'])
            serializer.save(**data)
        serializer.save()


    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.user)



class TempLink(View):
    def get(self, request, tmpimg):
        img = Image.objects.get(temp_id=tmpimg)
        if img.temp_link_expire_time >= datetime.now():
            return FileResponse(img.img)
        else:
            raise Http404
