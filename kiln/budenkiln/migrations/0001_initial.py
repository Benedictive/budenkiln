# Generated by Django 3.2.9 on 2021-12-21 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemperatureCurve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TemperaturePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.PositiveIntegerField()),
                ('temperature', models.PositiveIntegerField()),
                ('curve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budenkiln.temperaturecurve')),
            ],
        ),
        migrations.CreateModel(
            name='Kiln',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_curve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budenkiln.temperaturecurve')),
            ],
        ),
    ]
