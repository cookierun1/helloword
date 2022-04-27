# Generated by Django 3.2.13 on 2022-04-27 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system_manage', '0008_categoryl_categorys'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='wine',
            new_name='wm_wine',
        ),
        migrations.RenameField(
            model_name='monthwine',
            old_name='month_package',
            new_name='sm_month_package',
        ),
        migrations.RenameField(
            model_name='monthwine',
            old_name='wine',
            new_name='wn_wine',
        ),
        migrations.RenameField(
            model_name='shop',
            old_name='shop_grade',
            new_name='sma_shop_grade',
        ),
        migrations.RenameField(
            model_name='shopuser',
            old_name='shop',
            new_name='sm_shop',
        ),
        migrations.RenameField(
            model_name='todaywine',
            old_name='today_reg',
            new_name='sm_today_reg',
        ),
        migrations.RenameField(
            model_name='todaywine',
            old_name='wine',
            new_name='wm_wine',
        ),
        migrations.RenameField(
            model_name='wine',
            old_name='country',
            new_name='wma_country',
        ),
        migrations.RenameField(
            model_name='wine',
            old_name='grape',
            new_name='wma_grape',
        ),
        migrations.RenameField(
            model_name='wine',
            old_name='region',
            new_name='wma_region',
        ),
        migrations.RenameField(
            model_name='wine',
            old_name='winery',
            new_name='wma_winery',
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopItemNum', models.CharField(max_length=100, verbose_name='가맹점제품번호')),
                ('shopItemNameOne', models.CharField(max_length=100, null=True, verbose_name='가맹점제품명1')),
                ('shopItemNameTwo', models.CharField(max_length=100, null=True, verbose_name='가맹점제품명2')),
                ('shopItemImage', models.CharField(max_length=255, null=True, verbose_name='가맹점제품이미지')),
                ('shopItemVideo', models.CharField(max_length=255, null=True, verbose_name='가맹점제품동영상')),
                ('shopItemDes', models.TextField(null=True, verbose_name='가맹점제품설명')),
                ('shopItemPrice', models.IntegerField(verbose_name='가맹정제품가격')),
                ('shopItemQty', models.IntegerField(verbose_name='가맹정제품재고수량')),
                ('isWine', models.BooleanField(default=True, verbose_name='가맹점제품구분자')),
                ('createdDate', models.DateTimeField(auto_now_add=True, verbose_name='생성시간')),
                ('updatedDate', models.DateTimeField(auto_now=True, verbose_name='수정시간')),
                ('sm_cat_s', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system_manage.categorys')),
                ('sm_shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system_manage.shop')),
                ('wm_wine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='system_manage.wine')),
            ],
            options={
                'db_table': 'sm_item',
            },
        ),
    ]
