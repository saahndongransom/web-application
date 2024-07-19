from django.urls import path, include
from . import views

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('slide-section/', views.slide_section, name='slide_section'),
    path('footer.html', views.footer, name='footer'),
    path("newsletter", views.newsletter, name="newsletter"),
    path('', views.PostList.as_view(), name='home'),
    path('slide-section', views.slide_section, name='slide_section'),
    path('policy/', views.policy, name='policy'),
    path('mission.html', views.mission, name='mission'),
    path('newhatchtech.html', views.site, name='newhatchtech'),
    path('aboutme.html', views.aboutme, name='aboutme'),
    path('subscribe/', views.subscribe, name='subscribe_newsletter'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('home1/', views.home1, name="home1"),
    path('feli.html', views.feli, name='feli'),
    path('paypal_return/', views.paypal_return, name='paypal-return'),
    path('paypal-cancel/', views.paypal_cancel, name='paypal-cancel'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),  # Keep the post_detail for slug-based posts
    path('<int:pk>/', views.post_detail_with_pk, name='post_detail_with_pk'),  # Use a different pattern for post_detail with pk
    path('post_tag/<slug:tag_slug>/', views.post_tag, name='post_tag'),  # Use a separate pattern for post_tag view
]
