# Generated by Django 4.2 on 2023-06-06 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_post_postlikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postLikes',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
