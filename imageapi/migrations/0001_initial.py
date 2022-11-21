# Generated by Django 4.1.3 on 2022-11-18 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=20, verbose_name='Plan name')),
                ('canLinkOrig', models.BooleanField(default=False, verbose_name='Is linking the original image allowed in this plan?')),
                ('canCreateTempLink', models.BooleanField(default=False, verbose_name='Can user create an expiring link to the image?')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='imageapi.serviceplan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlanThumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(verbose_name='Height in pixels')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbs', to='imageapi.serviceplan')),
            ],
        ),
    ]
