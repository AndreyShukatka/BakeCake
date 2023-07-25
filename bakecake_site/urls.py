from django.urls import path
from bakecake_site import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('lk', views.LkPage.as_view(), name='lk'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)