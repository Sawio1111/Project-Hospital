# Generated by Django 4.1.1 on 2022-10-03 19:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_appointmentnotes_alter_opinion_author_delete_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentnotes',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opinion',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
