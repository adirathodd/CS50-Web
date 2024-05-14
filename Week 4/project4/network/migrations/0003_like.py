# Generated by Django 4.2 on 2023-06-06 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0)),
                ('users', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='likedUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
