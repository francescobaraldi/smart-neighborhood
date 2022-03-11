# Generated by Django 3.2.7 on 2022-03-11 13:29

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
            name='Casa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('via', models.CharField(max_length=50)),
                ('numero_civico', models.IntegerField()),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DatiAmbientali',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('potentiometer_value', models.FloatField()),
                ('photoresistor_value', models.FloatField()),
                ('thermometer_value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Finestra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stato', models.CharField(choices=[('open', 'Aperta'), ('closed', 'Chiusa')], max_length=10)),
                ('posizione', models.CharField(choices=[('nord', 'Nord'), ('sud', 'Sud')], max_length=10)),
                ('descrizione', models.CharField(max_length=50)),
                ('casa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.casa')),
            ],
        ),
    ]
