# Generated by Django 5.0.6 on 2024-06-16 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawls', '0005_filterrule_cumulative_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='filterset',
            name='remaining_urls',
            field=models.IntegerField(default=0),
        ),
    ]
