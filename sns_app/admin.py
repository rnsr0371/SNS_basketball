from django.contrib import admin
from .models import TweetModel,MemberModel,GoodModel

# Register your models here.
admin.site.register(TweetModel)
admin.site.register(MemberModel)
admin.site.register(GoodModel)