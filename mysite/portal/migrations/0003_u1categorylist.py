# Generated by Django 2.2.24 on 2021-11-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_u1members'),
    ]

    operations = [
        migrations.CreateModel(
            name='U1CategoryList',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('category', models.CharField(db_column='CATEGORY', max_length=100)),
                ('category_desc', models.CharField(blank=True, db_column='CATEGORY_DESC', max_length=100, null=True)),
            ],
            options={
                'db_table': 'U1_CATEGORY_LIST',
                'managed': False,
            },
        ),
    ]
