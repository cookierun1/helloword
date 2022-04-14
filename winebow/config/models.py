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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_no = models.CharField(db_column='phone_no', null=True, max_length=100, default='')
    usage_flag = models.CharField(max_length=10, default='1')
    name = models.CharField(db_column='name', max_length=100)

    class Meta:
        db_table = "auth_profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
