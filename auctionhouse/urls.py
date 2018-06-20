from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^product_list/$', views.product_list, name='product_list'),
    url(r'^login/$',
        auth_views.LoginView.as_view(   template_name="login.html",
                                        redirect_field_name="/product_list/",
                                        redirect_authenticated_user=True
                                        ),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page="/product_list/", redirect_field_name="/product_list/"), name='logout'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]
