# Generated by Django 2.2 on 2019-04-10 08:39

from django.db import migrations, models
import django.db.models.deletion
import sluggable.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', sluggable.fields.SluggableField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('slug', sluggable.fields.SluggableField()),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('slug', sluggable.fields.SluggableField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', sluggable.fields.SluggableField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(blank=True, max_length=50)),
                ('slug', sluggable.fields.SluggableField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('slug', models.CharField(db_index=True, max_length=255, verbose_name='URL')),
                ('redirect', models.BooleanField(default=False, verbose_name='Redirection')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('slug', models.CharField(db_index=True, max_length=255, verbose_name='URL')),
                ('redirect', models.BooleanField(default=False, verbose_name='Redirection')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', sluggable.fields.SluggableField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.User')),
            ],
        ),
        migrations.CreateModel(
            name='PollSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('slug', models.CharField(db_index=True, max_length=255, verbose_name='URL')),
                ('redirect', models.BooleanField(default=False, verbose_name='Redirection')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('slug', models.CharField(db_index=True, max_length=255, verbose_name='URL')),
                ('redirect', models.BooleanField(default=False, verbose_name='Redirection')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
