from django.db import models
from config.models import Profile
# 배송지관리
class ShipAddress(models.Model):
    auth_profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name='address')
    shipAddressName = models.CharField(max_length=100, verbose_name='배송지이름')
    shipAddress = models.CharField(null=True, max_length=255, verbose_name='회원현재주소')
    shipZipcode = models.CharField(null=True, max_length=20, verbose_name='배송지우편번호')
    shipUserName = models.CharField(null=True, max_length=100, verbose_name='수령인')
    shiopUserPhone = models.CharField(null=True, max_length=20, verbose_name='수령인연락처')
    shipDefault = models.BooleanField(default=False, verbose_name='기본배송지여부')
    regionDes = models.TextField(null=True, verbose_name='배송메모')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta:
        db_table = "profile_shipAddress"
