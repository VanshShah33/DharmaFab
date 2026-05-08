# Generated for connected lead, inquiry, and newsletter storage.

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dhrma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='company',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='consent',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='quantity',
            field=models.CharField(blank=True, default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='company',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inquiry',
            name='fabric_name',
            field=models.CharField(blank=True, default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='Dhrma.product',
            ),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='quantity',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
