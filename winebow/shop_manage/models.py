from django.db import models
from django.contrib.auth.models import User
from system_manage.models import Shop

# 가맹점회원관리
class ShopUser(models.Model):
    sm_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    isStaff = models.BooleanField(default=False, verbose_name='관리자승급')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_shop_user'