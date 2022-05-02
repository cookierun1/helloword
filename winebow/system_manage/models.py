from statistics import mode
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.query_utils import Q
from django.contrib.auth.models import User

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

# 서머노트
class Summernote(models.Model):
    title = models.CharField(max_length=100, null=True, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_summernote'

# 기준지역
class Region(models.Model):
    regionNameEn = models.CharField(max_length=100, verbose_name='지역이름영문')
    regionNameKr = models.CharField(max_length=100, verbose_name='지역이름한글')
    regionImg = models.ImageField(null=True, upload_to="image/wine_master/region/", verbose_name='지역이미지')
    regionDes = models.TextField(null=True, verbose_name='지역설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'wma_region'

# 생산국가
class Country(models.Model):
    countryNameEn = models.CharField(max_length=100, verbose_name='생산국가이름영문')
    countryNameKr = models.CharField(max_length=100, verbose_name='생산국가이름한글')
    countryImg = models.ImageField(null=True, upload_to="image/wine_master/country/", verbose_name='생산국가이미지')
    countryDes = models.TextField(null=True, verbose_name='생산국가설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'wma_country'

# 포도종류
class Grape(models.Model):
    grapeNameEn = models.CharField(max_length=100, verbose_name='포도이름영문')
    grapeNameKr = models.CharField(max_length=100, verbose_name='포도이름한글')
    grapeImg = models.ImageField(null=True, upload_to="image/wine_master/grape", verbose_name='포도이미지')
    grapeDes = models.TextField(null=True, verbose_name='포도설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'wma_grape'

# 와이너리
class Winery(models.Model):
    wineryNameEn = models.CharField(max_length=100, verbose_name='와이너리이름영문')
    wineryNameKr = models.CharField(max_length=100, verbose_name='와이너리이름한글')
    wineryImg = models.ImageField(null=True, upload_to="image/wine_master/winery/", verbose_name='와이너리이미지')
    wineryDes = models.TextField(null=True, verbose_name='외이너리설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'wma_winery'

# 와인마스터 TODO: 필드 추가 필요 미완성.
class Wine(models.Model):
    wma_region = models.ForeignKey(Region, on_delete=models.PROTECT)
    wma_grape = models.ForeignKey(Grape, on_delete=models.PROTECT)
    wma_winery = models.ForeignKey(Winery, on_delete=models.PROTECT)
    wma_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    wineNum = models.CharField(max_length=100, verbose_name='와인제품번호')
    wineNameEn = models.CharField(max_length=100, verbose_name='와인명영문')
    wineNameKr = models.CharField(max_length=100, verbose_name='와인명영문')
    wineImg = models.ImageField(null=True, upload_to="image/wine_master/wine/", verbose_name='와인이미지')
    wineDes = models.TextField(null=True, verbose_name='와인설명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'wm_wine'

# 이달의와인패키지설정
class MonthPackage(models.Model):
    packageName = models.CharField(max_length=100, verbose_name='패키지이름')
    startDate = models.DateTimeField(null=True, verbose_name='시작일')
    endDate = models.DateTimeField(null=True, verbose_name='종료일')
    packageImage = models.ImageField(null=True, upload_to="image/shop_master/package/", verbose_name='패키지이미지')
    packageStatus = models.BooleanField(default=False, verbose_name='진행현황')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_month_package'

# 이달의와인
class MonthWine(models.Model):
    wn_wine = models.ForeignKey(Wine, on_delete=models.PROTECT)
    sm_month_package = models.ForeignKey(MonthPackage, on_delete=models.PROTECT, related_name='month_wine')
    wineNum = models.CharField(max_length=100, verbose_name='제품번호')
    monthWinePrice = models.IntegerField(verbose_name='제품가격')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_month_wine'

# 오늘의와인설정
class TodayReg(models.Model):
    displayStartTime = models.DateTimeField(null=True, verbose_name='시작시간')
    displayEndTime = models.DateTimeField(null=True, verbose_name='종료시간')
    displayStatus = models.BooleanField(default=False, verbose_name='진행현황')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_today_reg'

# 오늘의와인
class TodayWine(models.Model):
    wm_wine = models.ForeignKey(Wine, on_delete=models.PROTECT)
    sm_today_reg = models.ForeignKey(TodayReg, on_delete=models.PROTECT, related_name='today_wine')
    wineNum = models.CharField(max_length=100, verbose_name='제품번호')
    todayWinePrice = models.IntegerField(verbose_name='제품가격')
    name = models.CharField(null=True, max_length=100, verbose_name='할인명')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_today_wine'

# 와인경매 TODO 이미지 날짜별 디렉토리분리
class Auction(models.Model):
    wm_wine = models.ForeignKey(Wine, on_delete=models.PROTECT, related_name='auction')
    auctionNumber = models.CharField(max_length=100, verbose_name='제품번호')
    actionImage1 = models.ImageField(null=True, upload_to="image/shop_master/auction/", verbose_name='와인이미지1')
    actionImage2 = models.ImageField(null=True, upload_to="image/shop_master/auction/", verbose_name='와인이미지2')
    actionImage3 = models.ImageField(null=True, upload_to="image/shop_master/auction/", verbose_name='와인이미지3')
    auctionStartTime = models.DateTimeField(null=True, verbose_name='시작시간')
    auctionEndTime = models.DateTimeField(null=True, verbose_name='종료시간')
    auctionStartPrice = models.IntegerField(verbose_name='경매시작가격')
    auctionBidPrice = models.IntegerField(verbose_name='제시금액단위')
    auctionFinalPrice = models.IntegerField(verbose_name='낙찰가격')
    auctionFinalUser = models.CharField(max_length=100, null=True, verbose_name='낙찰자')
    auctionStatus = models.BooleanField(default=False, verbose_name='경매상황')
    auctionDifferPrice = models.IntegerField(verbose_name='경매차액')
    auctionBidderNum = models.IntegerField(verbose_name='경매참가자수')
    auctionValuePrice = models.IntegerField(verbose_name='감정가')
    auctionCurrentPrice = models.IntegerField(verbose_name='현재가')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta :
        db_table = 'sm_auction'

# 경매참가자
class AuctionBidder(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sm_auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction_bidder')
    bidPirce = models.IntegerField(verbose_name='제시가')
    isBestBidder = models.BooleanField(default=False, verbose_name='낙찰여부')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_auction_bidder'

# 가맹점등급
class ShopGrade(models.Model):
    gradeName = models.CharField(max_length=100, verbose_name='등급이름')
    gradeLtdQty = models.IntegerField(verbose_name='상품등록개수')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sma_shop_grade'

# 가맹점
class Shop(models.Model):
    sma_shop_grade = models.ForeignKey(ShopGrade, on_delete=models.PROTECT, related_name='shop')
    shopName = models.CharField(max_length=100, verbose_name='가맹점이름')
    shopPhone = models.CharField(null=True, max_length=20, verbose_name='가맹점연락처')
    shopAddress = models.CharField(null=True, max_length=255, verbose_name='가맹점주소')
    shopRegNum = models.CharField(null=True, max_length=20, verbose_name='가맹점사업자등록번호')
    shopImage = models.ImageField(null=True, upload_to="image/shop_master/shop/", verbose_name='가맹점이미지')
    shopPointRatio = models.IntegerField(verbose_name='기본적립금비율')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_shop'

# 가맹점회원관리
class ShopUser(models.Model):
    sm_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE)
    isStaff = models.BooleanField(default=False, verbose_name='관리자승급')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_shop_user'

# 대분류
class CategoryL(models.Model):
    catLName = models.CharField(max_length=100, verbose_name='대분류이름')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_cat_l'

# 소분류
class CategoryS(models.Model):
    cat_l = models.ForeignKey(CategoryL, on_delete=models.CASCADE)
    catSName = models.CharField(max_length=100, verbose_name='소분류이름')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_cat_s'

# 가맹점아이템마스터 TODO: 필드 추가 필요 미완성
class Item(models.Model):
    sm_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    wm_wine = models.ForeignKey(Wine, on_delete=models.PROTECT)
    sm_cat_s = models.ForeignKey(CategoryS, on_delete=models.PROTECT)
    shopItemNum = models.CharField(max_length=100, verbose_name='가맹점제품번호')
    shopItemNameOne = models.CharField(null=True, max_length=100, verbose_name='가맹점제품명1')
    shopItemNameTwo = models.CharField(null=True, max_length=100, verbose_name='가맹점제품명2')
    shopItemImage = models.ImageField(null=True, upload_to="image/shop_master/item/", verbose_name='가맹점제품이미지')
    shopItemVideo = models.FileField(null=True, upload_to="video/shop_master/item/%Y/%m/%d/", verbose_name='가맹점제품동영상')
    shopItemDes = models.TextField(null=True, verbose_name='가맹점제품설명')
    shopItemPrice = models.IntegerField(verbose_name='가맹정제품가격')
    shopItemQty = models.IntegerField(verbose_name='가맹정제품재고수량')
    isWine = models.BooleanField(default=True, verbose_name='가맹점제품구분자')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta : 
        db_table = 'sm_item'

# 맴버쉽아이템
class MPItem(models.Model):
    sm_item = models.ForeignKey(Item, on_delete=models.PROTECT)
    MPPrice= models.IntegerField(verbose_name='차감포인트')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')
    class Meta : 
        db_table = 'wma_mp_item'