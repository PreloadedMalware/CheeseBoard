from django.contrib import admin
from CheeseBoardSite.models import Account, Cheese, Badge, Saved, Post, Comment, Stats
from django.contrib.auth.models import User

class AccountAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('user',)}


admin.site.register(Account, AccountAdmin)
admin.site.register(Cheese)
admin.site.register(Badge)
admin.site.register(Saved)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Stats)
# Register your models here.