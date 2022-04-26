from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.db.models.signals import post_save
from django.dispatch import receiver


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    deleted_at = models.DateTimeField(null=True, verbose_name='삭제시간')

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(using=using)
        return

    class Meta:
        abstract = True

# 유저
class Profile(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    userNickname = models.CharField(null=True, max_length=100, verbose_name='회원닉네임')
    userCurrentAddress = models.CharField(null=True, max_length=255, verbose_name='회원현재주소')
    userCurrentZip = models.CharField(null=True, max_length=20, verbose_name='회원현재우편번호')
    userPhone = models.CharField(null=True, max_length=20, verbose_name='회원연락처')
    userBirth = models.DateField(default=None, verbose_name='회원생년월일')
    userGender = models.CharField(null=True, max_length=10, verbose_name='회원성별')
    userPoint = models.IntegerField(default=0, verbose_name='회원적립금')
    userMemberPoint = models.IntegerField(default=0, verbose_name='회원맴버쉽포인트')
    userAgreeGeneral = models.BooleanField(default=True, verbose_name='이용약관동의')
    userAgreePrivate = models.BooleanField(default=True, verbose_name='개인정보수집동의')
    userAgreePromotion = models.BooleanField(default=True, verbose_name='이벤트 프로모션동의')
    emailVerified = models.BooleanField(default=False, verbose_name='이메일인증')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta:
        db_table = "auth_profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
