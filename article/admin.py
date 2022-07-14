from django.contrib import admin
from .models import Article, Apply, Review, ArticleCategory
# Register your models here.

admin.site.register(Article)
admin.site.register(Apply)
admin.site.register(Review)
admin.site.register(ArticleCategory)