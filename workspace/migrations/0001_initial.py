# Generated by Django 4.1.3 on 2023-01-26 14:59

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
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
                ('adventure_type', models.CharField(choices=[('Beach and ocean', 'Beach and ocean'), ('City attractions', 'City attractions'), ('Sport event', 'Sport event'), ('Outdoor activities', 'Outdoor activities'), ('Food and restaurants', 'Food and restaurants'), ('Historical landmarks', 'Historical landmarks')], max_length=50)),
                ('climate', models.CharField(choices=[('Tropical', 'Tropical'), ('Subtropical', 'Subtropical'), ('Temperate', 'Temperate'), ('Desert', 'Desert'), ('Mediterranean', 'Mediterranean'), ('Highlands', 'Highlands'), ('Polar', 'Polar')], max_length=50)),
                ('flight', models.CharField(choices=[('Quick', 'Quick'), ('Short', 'Short'), ('Medium', 'Medium'), ('Long', 'Long'), ('Very long', 'Very long')], max_length=50)),
                ('notes', models.TextField(blank=True)),
                ('activity1', models.TextField(blank=True)),
                ('activity2', models.TextField(blank=True)),
                ('activity3', models.TextField(blank=True)),
                ('activity4', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, default='user_destination_images/default.png', upload_to='user_destination_images/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('has_user_visited', models.BooleanField(blank=True, default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Destinations',
                'ordering': ('city',),
            },
        ),
    ]
