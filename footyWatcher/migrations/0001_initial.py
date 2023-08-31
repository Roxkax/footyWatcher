# Generated by Django 4.2.4 on 2023-08-31 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team', models.CharField(max_length=200)),
                ('away_team', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footyWatcher.competition')),
            ],
        ),
        migrations.CreateModel(
            name='GameUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=500)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='footyWatcher.game')),
            ],
        ),
    ]