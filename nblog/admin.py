#from .models import Post,Tag
from django.contrib import admin
from .models import Post,Comment
from .models import  SubscribedUsers
from .models import Category


from django.forms.widgets import TextInput
from django.urls import reverse
from django.utils.safestring import mark_safe




#from.models import Comment



# Customize the way the admin panel looks
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')  # displays the properties mentioned in the tuple
    list_filter = ('created_on',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')



class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_date', 'post', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('name', 'email', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class CKEditorWidget(TextInput):
    template_name = 'admin/ckeditor_widgets'









# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(SubscribedUsers, SubscribedUsersAdmin,)

admin.site.register(Category)

#admin.site.register([Tag])
admin.site.register(Comment)
#admin.site.register (tags)
#admin.site.register(Tag)







