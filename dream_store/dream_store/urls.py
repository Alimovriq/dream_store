from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls.products_urls')),
    path('api/v1/', include('api.urls.shop_basket_urls')),
    path('api/v1/', include('api.urls.orders_urls')),
    path('api/v1/', include('api.urls.orders_refund_urls')),
    path('api/v1/', include('api.urls.users_urls')),
    path('api/v1/', include('api.urls.news_urls')),
    path('api/v1/', include('api.urls.payment_urls'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
