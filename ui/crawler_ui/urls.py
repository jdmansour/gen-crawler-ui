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
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets

from crawls.models import CrawlJob, CrawledURL, FilterSet, FilterRule
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


class FilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilterRule
        fields = ['id', 'filter_set', 'rule', 'include', 'created_at', 'updated_at', 'page_type', 'count', 'position']
        # order rules by position, ascending
    
    

class InlineFilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for FilterRule, omits the urls of the rule and the set. """
    class Meta:
        model = FilterRule
        fields = ['id', 'rule', 'include', 'created_at', 'updated_at', 'page_type', 'count', 'position']
        


class FilterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterSet
        fields = ['id', 'crawl_job', 'name', 'created_at', 'updated_at', 'url', 'rules']
        depth = 1

    # order rules by position, ascending
    rules = serializers.SerializerMethodField('get_rules')

    def get_rules(self, obj):
        rules = obj.rules.order_by('position')
        return InlineFilterRuleSerializer(rules, many=True, context=self.context).data


class FilterSetViewSet(viewsets.ModelViewSet):
    queryset = FilterSet.objects.all()
    serializer_class = FilterSetSerializer


class FilterRuleViewSet(viewsets.ModelViewSet):
    queryset = FilterRule.objects.all()
    serializer_class = FilterRuleSerializer
    # filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    # ordering_fields = ['position']
    # ordering = ['position']

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).order_by('position')


    # run code when a new rule is created
    # set count to 34
    # call "evaluate" on the filterset
    def perform_create(self, serializer: FilterRuleSerializer):
        rule = serializer.save()
        rule.filter_set.evaluate()
        # TODO: in what is returned in the request, the new count is not reflected yet (?)
        rule.save()  # ?

    def perform_update(self, serializer: FilterRuleSerializer):
        rule = serializer.save()
        rule.filter_set.evaluate(rule)
        rule.save()

router.register(r'filter_sets', FilterSetViewSet)
router.register(r'filter_rules', FilterRuleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
