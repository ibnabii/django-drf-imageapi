from rest_framework import serializers
from rest_framework.reverse import reverse

from imageapi.models import ServicePlan, Image, ImageThumbnail, PlanThumbnail, Profile




class ServicePlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServicePlan
        fields = '__all__'

    # id = serializers.ReadOnlyField()
    thumbnail_sizes = serializers.SerializerMethodField()

    def get_thumbnail_sizes(self, obj):
        return obj.thumbs.all().values_list('height', flat=True)


class ImageThumbnailSerializer(serializers.HyperlinkedModelSerializer):
    # size = PlanThumbnailSerializer()
    size = serializers.SlugRelatedField(
        read_only=True,
        slug_field='height'
    )
    class Meta:
        model = ImageThumbnail
        fields = ('img', 'size', )


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        exclude = ['owner', 'temp_id', ]
        read_only_fields = ['temp_link', 'temp_link_expire_time']

    thumbnails = ImageThumbnailSerializer(required=False, many=True, read_only=True)




    def __init__(self, *args, **kwargs):
        super(ImageSerializer, self).__init__(*args, **kwargs)
        if not ServicePlan.objects.get(pk=
                                       Profile.objects.get(user=self.context['request'].user).plan.id
                                       ).canLinkOrig:
            if 'img' not in self.Meta.exclude:
                self.Meta.exclude += ['img']
        else:
            if 'img' in self.Meta.exclude:
                self.Meta.exclude.remove('img')

        if not ServicePlan.objects.get(pk=
                                       Profile.objects.get(user=self.context['request'].user).plan.id
                                       ).canCreateTempLink:
            if 'temp_link_longevity' not in self.Meta.exclude:
                self.Meta.exclude += ['temp_link_longevity']
        else:
            if 'temp_link_longevity' in self.Meta.exclude:
                self.Meta.exclude.remove('temp_link_longevity')

