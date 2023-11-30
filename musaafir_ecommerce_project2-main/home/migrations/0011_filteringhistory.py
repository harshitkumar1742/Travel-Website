# Generated by Django 3.0.14 on 2022-01-06 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20220106_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteringHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup', models.CharField(blank=True, max_length=200, null=True)),
                ('pickup_datetime', models.DateTimeField(blank=True, null=True)),
                ('destination', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Customer')),
            ],
        ),
    ]
