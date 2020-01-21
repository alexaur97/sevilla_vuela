# Generated by Django 2.2.7 on 2020-01-20 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aerolinea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=15)),
                ('logo', models.URLField()),
                ('email', models.EmailField(max_length=254, null=True)),
                ('url_web', models.URLField()),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.CreateModel(
            name='Vuelo',
            fields=[
                ('codigo_vuelo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('Aterrizó', 'Aterrizo'), ('Programado', 'Programado'), ('En Ruta', 'En Ruta')], max_length=30)),
                ('con_retraso', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Llegada_comp',
            fields=[
                ('vuelo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Vuelo')),
                ('aerolinea', models.CharField(max_length=50)),
                ('origen', models.CharField(max_length=50)),
                ('hora_llegada', models.CharField(max_length=10, verbose_name='Hora de llegada')),
                ('operadora', models.CharField(max_length=50)),
            ],
            bases=('main.vuelo',),
        ),
        migrations.CreateModel(
            name='Salida_comp',
            fields=[
                ('vuelo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Vuelo')),
                ('aerolinea', models.CharField(max_length=50)),
                ('destino', models.CharField(max_length=50)),
                ('partida', models.CharField(max_length=10, verbose_name='Hora de salida')),
                ('operadora', models.CharField(max_length=50)),
            ],
            bases=('main.vuelo',),
        ),
        migrations.CreateModel(
            name='Salida',
            fields=[
                ('vuelo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Vuelo')),
                ('destino', models.CharField(max_length=50)),
                ('partida', models.CharField(max_length=10, verbose_name='Hora de salida')),
                ('aerolinea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Aerolinea')),
            ],
            bases=('main.vuelo',),
        ),
        migrations.CreateModel(
            name='Llegada',
            fields=[
                ('vuelo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.Vuelo')),
                ('origen', models.CharField(max_length=50)),
                ('hora_llegada', models.CharField(max_length=10, verbose_name='Hora de llegada')),
                ('aerolinea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Aerolinea')),
            ],
            bases=('main.vuelo',),
        ),
    ]
