# Generated by Django 3.2.13 on 2022-05-03 11:33

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
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userNickname', models.CharField(max_length=100, null=True, verbose_name='회원닉네임')),
                ('userCurrentAddress', models.CharField(max_length=255, null=True, verbose_name='회원현재주소')),
                ('userCurrentZip', models.CharField(max_length=20, null=True, verbose_name='회원현재우편번호')),
                ('userPhone', models.CharField(max_length=20, null=True, verbose_name='회원연락처')),
                ('userImage', models.ImageField(null=True, upload_to='image/profile/', verbose_name='회원이미지')),
                ('userBirth', models.DateField(default=None, null=True, verbose_name='회원생년월일')),
                ('userGender', models.CharField(max_length=10, null=True, verbose_name='회원성별')),
                ('userCompanyName', models.CharField(max_length=100, null=True, verbose_name='회사명')),
                ('userDelFlag', models.BooleanField(default=False, verbose_name='회원탈퇴플래그')),
                ('userDelDate', models.DateTimeField(null=True, verbose_name='회원탈퇴일')),
                ('userPoint', models.IntegerField(default=0, verbose_name='회원적립금')),
                ('userMemberPoint', models.IntegerField(default=0, verbose_name='회원맴버쉽포인트')),
                ('userAgreeGeneral', models.BooleanField(default=True, verbose_name='이용약관동의')),
                ('userAgreePrivate', models.BooleanField(default=True, verbose_name='개인정보수집동의')),
                ('userAgreePromotion', models.BooleanField(default=True, verbose_name='이벤트 프로모션동의')),
                ('updatedDate', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_profile',
            },
        ),
    ]
