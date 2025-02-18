# Generated by Django 5.0.6 on 2024-06-14 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterSet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FilterRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField()),
                ('include', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('page_type', models.CharField(default='', max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('filter_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawls.filterset')),
            ],
        ),
    ]
