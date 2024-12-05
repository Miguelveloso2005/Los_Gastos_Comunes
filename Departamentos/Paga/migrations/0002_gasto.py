# Generated by Django 5.1.3 on 2024-12-02 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Paga', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gasto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pagado', models.BooleanField(default=False)),
            ],
        ),
    ]