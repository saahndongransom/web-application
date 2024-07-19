from django.shortcuts import render, redirect
from django.views import generic
from .models import Post
from django.views.generic import View
from django.views.generic import ListView
#from django.views.generic import PostList
from django.core.paginator import Paginator
#from .forms import CommentForm
from django.views.generic.detail import DetailView
from .form import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import SubscribedUsers
from django.contrib import messages
from django.core.mail import EmailMessage
from .form import NewsletterForm
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse
from  django . core.mail import send_mail

from django.contrib import messages
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

#from .models import Tag
from django.core.paginator import Paginator
import json

from django.core import serializers
from django.http import JsonResponse
#from django.core.paginator import paginator
from django.shortcuts import render
#from .models import post
from django.http import JsonResponse
from .models import Post, Comment
from .form import CommentForm

from nblog.models import Category
from nblog.form import CategoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


from django.core.paginator import Paginator
from django.shortcuts import render
from nblog.models import Post, Category

# views.py
from django.shortcuts import render, get_object_or_404
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
from .models import Post
from django.utils.html import strip_tags
from django import template
from .form import ContactForm
from django.core.mail import send_mail
#from nblog.models import RelatedPost



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'nblog/index.html'
    context_object_name = 'posts'
    paginate_by = 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_posts'] = Post.objects.filter(status=1).order_by('-created_on')[:5]
        return context
    

class CategoryView(ListView):
    model = Post
    template_name = 'nblog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       # post = self.get_object()
       # related_posts = post.related_posts()
        #context['related_posts'] = related_posts
        return context



#class PostDetail(generic.DetailView):
       #model = Post
       #template_name = 'nblog/post_detail.html'
def post_detail(request, slug):
    print(f"Slug value: {slug}")
    post = get_object_or_404(Post, slug=slug)
    
    context = {'post': post}

    featured_posts = Post.objects.filter(status=1).order_by('-created_on')[:2]
    context = {'post': post, 'featured_posts': featured_posts}
    return render(request, 'nblog/post_detail.html', context)



#def post_detail(request, slug):
 #   post = get_object_or_404(Post, slug=slug)
  #  return render(request, 'blog/post_detail.html', {'post': post})
#def PostDetail(request,slug):
   # post=get_object_or_404(Post,slug=slug)
    #return render(request,'nblog/post_detail.html',{'post':post})
def post_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = Post.objects.filter(tag=tag)
    print(post_list)  # Add this line to see if post_list is empty
    return render(request, 'nblog/post_tag.html', {'post_list': post_list})




    #return redirect('/')


def policy(request):
    return render(request , 'nblog/policy.html',{'policy': policy} )
def site(request):
    return render(request, 'nblog/site.html',{'site': site})
def aboutme(request):
    return render(request,'nblog/aboutme.html',{'aboutme':aboutme})
def mission(request):
    return render(request,'nblog/mission.html',{'mission':mission})
def footer(request):
    return render(request,'nblog/footer.html',{'footer':footer})

def subscribe(request):
    print(request.method)
    print(request.method, "method")
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, "You must type legit name and email to subscribe to a Newsletter")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            print(f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            print(f"{email} email address is already subscriber.")
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers(email=email)
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))

 #paypal
def feli(request):
    host = request.get_host()
    paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount': '%.20.0f',
            'item_name': "product 1",
            'invoice': "str(uuid.uuid4())",
            'currency_code': 'USD',
            'notify_url':f'http://{host}{reverse("paypal-ipn")}',
            'return_url':f'http://{host}{reverse("paypal-return")}',
            'cancel_return':f'http://{host}{reverse("paypal-cancel")}',


    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    contact = {'form':form}
    return render(request,'nblog/feli.html',contact)

def paypal_return(request):
    messages.success(request="you/ succefully make payment")
    return redirect('home')

def paypal_cancel(request):
    messages.error(request="you/ succefully make payment")
    return redirect('home')
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # Code to send email
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            email_from = request.user.email if request.user.is_authenticated else form.cleaned_data.get('email')
            # If the user is authenticated, use their email from the request.user object
            # Otherwise, use the email entered in the form

            if subject is None or email_message is None or email_from is None:
                messages.error(request, "One or more required fields are missing")
            else:
                mail = EmailMessage(subject, strip_tags(email_message), email_from, bcc=receivers)
                mail.content_subtype = 'html'

                if mail.send():
                    send_mail(
                        subject,
                        '',
                        '',
                        receivers,
                        html_message=email_message,
                        fail_silently=False,
                    )
                    messages.success(request, "Email sent successfully")
                else:
                    messages.error(request, "There was an error sending email")
        else:
            # Handle case where form is not valid
            email_message = ''
            for error in list(form.errors.values()):
                messages.error(request, error)
            messages.error(request, "There was an error sending email")

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='nblog/newsletter.html', context={'form': form})


def sanitize_address(addr, encoding):
    nm, addr = parseaddr(addr)
    if nm:
        nm = Header(nm, encoding).encode()
    if addr:
        localpart, domain = addr.split('@', 1)
        if localpart:
            localpart = quote(localpart.encode('utf-8'), safe='!#$%&\'*+-/=?^_`{|}~:')
        if domain:
            domain = domain.encode('idna').decode('ascii')
    else:
        localpart = ''
        domain = ''
    return formataddr((nm, localpart + '@' + domain))

def home1(request):
   return render(request,'nblog/home1.html',{'home1':home1})


# views.py

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)

    featured_posts = Post.objects.filter(status=1).order_by('-created_on')[:1]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

    context = {'post': post, 'comments': comments, 'form': form, 'featured_posts': featured_posts}
    return render(request, 'nblog/post_detail.html', context)

def category(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category=category).order_by('-published_date')

    paginator = Paginator(posts, 10) # paginate the posts by 10

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'category': category, 'page_obj': page_obj}
    return render(request, 'nblog/category.html', context)






    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        # Check the related name for the tag field
        print(post.tag.related_name)
        # Filter related posts by category and tag
        related_posts = Post.objects.filter(
            category=post.category
        ).filter(
            tag__in=post.tag.all()
        ).exclude(
            id=post.id
        ).distinct()
        context['related_posts'] = related_posts
        return context






'''def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    vectorizer = TfidfVectorizer()
    corpus = [post.content] + list(Post.objects.exclude(pk=pk).values_list('content', flat=True))
    tfidf = vectorizer.fit_transform(corpus)
    sim_scores = cosine_similarity(tfidf[0], tfidf[1:])[0]
    related_posts = Post.objects.exclude(pk=pk).order_by('-created_on')[:5]
    return render(request, 'nblog/post_detail.html', {'post': post, 'related_posts': related_posts})

# post_detail.html
'''


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']

            # Send the email
            subject = 'Contact form submission from {}'.format(name)
            body = 'Name: {}\nEmail: {}\nPhone number: {}\nMessage: {}'.format(name, email, phone_number, message)
            sender = 'saahransom@yahoo.com'
            recipients = ['saahndongransom@gmail.com']
            send_mail(subject, body, sender, recipients)

            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'nblog/contact.html', {'form': form})




def contact_success(request):
    return render(request, 'nblog/contact_success.html')


def home(request):
    return render(request, 'home.html')


#def post_detail(request, slug):
    #post = get_object_or_404(Post, slug=slug)
    #featured_posts = Post.objects.filter(status=1).order_by('-created_on')[:5]
    #context = {'post': post, 'featured_posts': featured_posts}
    #return render(request, 'nblog/post_detail.html', context)
from django.shortcuts import render

def slide_section(request):
    slide_section_data = "Some data for the slide section"  # Replace this with your actual data
    
    context = {
        'slide_section_data': slide_section_data
    }
    
    return render(request, 'nblog/slide_section.html', context)


def post_detail_with_pk(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Add any additional logic to handle the post with pk
    return render(request, 'post_detail_with_pk.html', {'post': post})

