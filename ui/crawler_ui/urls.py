"""
URL configuration for crawler_ui project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from crawls.views import (CrawlerViewSet, FilterRuleViewSet,
                          FilterSetViewSet, HealthViewSet, crawler_status_stream,
                          start_content_crawl, SourceItemViewSet, CrawlJobViewSet)
from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import index, wlo_spa

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'crawlers', CrawlerViewSet)
router.register(r'crawl_jobs', CrawlJobViewSet)
router.register(r'source_items', SourceItemViewSet)
router.register(r'filter_sets', FilterSetViewSet)
router.register(r'filter_rules', FilterRuleViewSet)
router.register(r'health', HealthViewSet, basename='health')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', index, name='index'),
    path('wlo_spa/', wlo_spa, name='wlo_spa'),
    # todo: is this used?
    path('filters/<int:pk>/crawl/', start_content_crawl, name='filterset_start_crawl'),
    path('admin/', admin.site.urls),
    path('api/crawlers/<int:crawler_id>/status_stream/', crawler_status_stream, name='crawler_status_stream'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("accounts/", include("django.contrib.auth.urls")),
] + debug_toolbar_urls()
