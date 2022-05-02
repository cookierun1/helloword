from django.db import models
from django.contrib.auth.models import User
from config.models import Profile
from system_manage.models import Wine, Summernote, BoardType, Shop

# 배송지관리
class ShipAddress(models.Model):
    auth_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='address')
    shipAddressName = models.CharField(max_length=100, verbose_name='배송지이름')
    shipAddress = models.CharField(null=True, max_length=255, verbose_name='회원현재주소')
    shipZipcode = models.CharField(null=True, max_length=20, verbose_name='배송지우편번호')
    shipUserName = models.CharField(null=True, max_length=100, verbose_name='수령인')
    shopUserPhone = models.CharField(null=True, max_length=20, verbose_name='수령인연락처')
    shipDefault = models.BooleanField(default=False, verbose_name='기본배송지여부')
    shipMemo = models.TextField(null=True, verbose_name='배송메모')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "profile_shipAddress"

# 와인리뷰
class WineReview(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    wm_wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    reviewMemo = models.TextField(null=True, verbose_name='메모')
    reviewRate = models.FloatField(default=5, verbose_name='평점')
    reviewPrice = models.IntegerField(verbose_name='구매가격')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "wma_review"

# 게시판
class Board(models.Model):
    sm_board_type = models.ForeignKey(BoardType, on_delete=models.PROTECT)
    sm_summernore = models.ForeignKey(Summernote, on_delete=models.PROTECT)
    sm_shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    boardViewCount = models.IntegerField(default=0, verbose_name='조회수')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "sm_board"

# 게시판댓글
class BoardComment(models.Model):
    sm_board = models.ForeignKey(Board, on_delete=models.CASCADE)
    boardComment = models.TextField(verbose_name='댓글내용')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "sm_board_comment"

# 게시판댓글답변
class BoardReply(models.Model):
    sm_board_comment = models.ForeignKey(Board, on_delete=models.PROTECT)
    boardReply = models.TextField(verbose_name='답변내용')
    createdDate = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updatedDate = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        db_table = "sm_board_reply"