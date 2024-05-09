from django.contrib import admin
from django.urls import path, include
from foodapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('<int:item_id>/', detail, name='detail'),
    path('about/', about, name='about'),
    path('home/', home, name='home'),
    path('profile/', profile, name='profile'),
    path('update/<int:id>/', update_item, name='update'),
    path('delete/<int:id>/', delete_item, name='delete'),
    path('add/', add_item, name='add'),
    
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profileupdate/', profile_update, name='profile_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
