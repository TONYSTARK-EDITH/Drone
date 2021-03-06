# Generated by Django 4.0.4 on 2022-05-16 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CBA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=1000)),
                ('phoneNumber', models.IntegerField()),
                ('emergencyValue', models.IntegerField()),
                ('files', models.FileField(upload_to='')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'verbose_name_plural': 'CBA',
            },
        ),
    ]
