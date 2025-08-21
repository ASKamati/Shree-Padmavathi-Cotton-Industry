"""cotton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cotton_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('reg',views.reg,name='reg'),
    path('forgotpass',views.forgotpass,name='forgotpass'),
    path('otp',views.otp,name='otp'),
    path('resetpass',views.resetpass,name='resetpass'),
    path('changepass',views.changepass,name='changepass'),
    path('get-cotton-count/', views.get_new_cotton_count, name='get_cotton_count'),

    path('add_dealers',views.add_dealers,name='add_dealers'),
    path('dealers_view',views.dealers_view,name='dealers_view'),
    path('cotton_req_del/<int:pk>',views.cotton_req_del,name='cotton_req_del'),
    path('market_del/<int:pk>',views.market_del,name='market_del'),
    path('market_edit/<int:pk>',views.market_edit,name='market_edit'),


    path('cotton_separation',views.cotton_separation,name='cotton_separation'),
    path('cotton_separation_view',views.cotton_separation_view,name='cotton_separation_view'),

    path('market_price',views.market_price,name='market_price'),
    path('reg_view',views.reg_view,name='reg_view'),
    path('login',views.login,name='login'),
    path('user_home',views.user_home,name='user_home'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('market_price_view',views.market_price_view,name='market_price_view'),
    path('market_price_view_u',views.market_price_view_u,name='market_price_view_u'),
    path('cotton_request',views.cotton_request,name='cotton_request'),
    path('cotton_request_view',views.cotton_request_view,name='cotton_request_view'),
    path('cotton_request_view_a', views.cotton_request_view_a, name='cotton_request_view_a'),
    path('approve_request/<int:pk>', views.approve_request, name='approve_request'),
    path('update_received_status/<int:pk>', views.update_received_status, name='update_received_status'),
    path('received_cottons', views.received_cottons, name='received_cottons'),

    path('farmers_payment', views.farmers_payment, name='farmers_payment'),
    path('farmer_payment_next/<int:pk>', views.farmer_payment_next, name='farmer_payment_next'),
    path('payment_msg', views.payment_msg, name='payment_msg'),
    path('payment_view_farmer', views.payment_view_farmer, name='payment_view_farmer'),
    path('payment_view_admin', views.payment_view_admin, name='payment_view_admin'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('view_farmer/<str:email>',views.view_farmer,name='view_farmer'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

