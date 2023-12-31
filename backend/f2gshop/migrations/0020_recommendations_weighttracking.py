# Generated by Django 4.0.1 on 2023-02-17 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('f2gshop', '0019_product_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendations',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('left_hand_side', models.TextField()),
                ('right_hand_side', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WeightTracking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_logged', models.DateTimeField(auto_now_add=True)),
                ('weightkg', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
