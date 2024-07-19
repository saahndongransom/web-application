
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from .models import Post,Category
from django import forms
from .models import Comment
#from .models import post



from django import forms
from .models import Contact

from nblog.models import Category





def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_number', 'message']



class NewsletterForm(forms.Form):
    
    subject = forms.CharField()
    receivers = forms.CharField()
    message = forms.CharField(widget=TinyMCE(), label="Email content")


    class Meta:
        fields = ('content', )

#class CommentForm(forms.ModelForm):

 #   class Meta:
  #      model = Comment
   #     fields = ('name', 'email', 'text')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'text')

    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)



class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ('title', 'content', 'categories')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']






