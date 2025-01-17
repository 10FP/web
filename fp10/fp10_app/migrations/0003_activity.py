# Generated by Django 3.2.25 on 2024-05-29 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fp10_app', '0002_customuser_online_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='activities/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_activities', to=settings.AUTH_USER_MODEL)),
                ('partitions', models.ManyToManyField(blank=True, related_name='participating_activities', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
