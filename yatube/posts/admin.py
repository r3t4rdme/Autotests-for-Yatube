from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text", "title", "group")
    list_filter = ("pub_date", "author", "group")
    empty_value_display = ("-пусто-")


admin.site.register(Post, PostAdmin)
admin.site.register(Group)