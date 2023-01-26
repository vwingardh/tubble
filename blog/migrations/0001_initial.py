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
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, 'Draft'), (1, 'Publish')], default=0)),
                ('featured', models.BooleanField(default=False)),
                ('blog_img', models.ImageField(upload_to='blog/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, related_name='blog_favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_comments', to='blog.blog')),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]