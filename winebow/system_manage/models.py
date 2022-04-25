from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q

# Create your models here.
class AccessPermissionManager(models.Manager):
    def get_queryset(self):
        return super(AccessPermissionManager, self).\
            get_queryset().filter(
                Q(content_type=AccessPermission.PERMISSION_TYPE.READ) |
                Q(content_type=AccessPermission.PERMISSION_TYPE.WRITE)
            )


class AccessPermission(Permission):
    """Proxy model for permission"""

    class Meta:
        proxy = True

    class __PERMISSION_TYPE:
        def get_all_permissions(self):
                    """Get list of all permissions."""
                    return [
                        self.READ,
                        self.WRITE
                    ]

        @property
        def WRITE(self):
            return ContentType.objects.get_or_create(
                app_label='write',
                model="write_permission",
            )[0]

        @property
        def READ(self):
            return ContentType.objects.get_or_create(
            app_label='read',
            model='read_permission',
            )[0]

    PERMISSION_TYPE = __PERMISSION_TYPE()
    objects = AccessPermissionManager()
    
    def save(self, *args, **kwargs):
        # Check Permission Type.
        if self.content_type not in self.PERMISSION_TYPE.get_all_permissions():
            raise ValueError('Not permitted Permission Type.')
        
        # ct, created = ContentType.objects.get_or_create(
        #     model=self._meta.verbose_name, app_label=self._meta.app_label,
        # )


        #self.content_type = ct
        super(AccessPermission, self).save(*args)


class Region(models.Model):
    regionNameEn = models.CharField(max_length=100, verbose_name='지역이름영문')
    regionNameKr = models.CharField(max_length=100, verbose_name='지역이름한글')
    regionImg = models.CharField(max_length=255, null=True, verbose_name='지역이미지')
    regionDes = models.TextField(null=True, verbose_name='지역설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta :
        db_table = 'wma_region'

class Country(models.Model):
    countryNameEn = models.CharField(max_length=100, verbose_name='생산국가이름영문')
    countryNameKr = models.CharField(max_length=100, verbose_name='생산국가이름한글')
    countryImg = models.CharField(max_length=255, null=True, verbose_name='생산국가이미지')
    countryDes = models.TextField(null=True, verbose_name='생산국가설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta :
        db_table = 'wma_country'

class Grape(models.Model):
    grapeNameEn = models.CharField(max_length=100, verbose_name='포도이름영문')
    grapeNameKr = models.CharField(max_length=100, verbose_name='포도이름한글')
    grapeImg = models.CharField(max_length=255, null=True, verbose_name='포도이미지')
    grapeDes = models.TextField(null=True, verbose_name='포도설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta :
        db_table = 'wma_grape'

class Winery(models.Model):
    wineryNameEn = models.CharField(max_length=100, verbose_name='와이너리이름영문')
    wineryNameKr = models.CharField(max_length=100, verbose_name='와이너리이름한글')
    wineryImg = models.CharField(max_length=255, null=True, verbose_name='와이너리이미지')
    wineryDes = models.TextField(null=True, verbose_name='외이너리설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta :
        db_table = 'wma_winery'

class Wine(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='region')
    grape = models.ForeignKey(Grape, on_delete=models.PROTECT, related_name='grape')
    winery = models.ForeignKey(Winery, on_delete=models.PROTECT, related_name='winery')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='country')
    wineNum = models.CharField(max_length=100, verbose_name='와인제품번호')
    wineNameEn = models.CharField(max_length=100, verbose_name='와인명영문')
    wineNameKr = models.CharField(max_length=100, verbose_name='와인명영문')
    wineImg = models.CharField(max_length=255, null=True, verbose_name='와인이미지')
    wineDes = models.TextField(null=True, verbose_name='와인설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성시간')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정시간')

    class Meta :
        db_table = 'wm_wine'