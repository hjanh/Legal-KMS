"""legal_mining URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from haystack.views import basic_search 
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from document_manager.forms import CustomSearchForm
from document_manager import views as dm_views
from document_manager.views import DocumentDetailView, upvote, downvote, delete, get_user_profile, recommendations, entity_search, paragraph_search
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from django.views.generic import TemplateView
sqs = sqs = SearchQuerySet().all()

urlpatterns = [
    url(r'^upvote/', upvote, name='upvote'),
    url(r'^downvote/', downvote, name='downvote'),
    url(r'^delete/', delete, name='delete'),
    url(r'^crawler/$', TemplateView.as_view(template_name="document_manager/crawler.html", content_type="text/html")),
    url(r'^admin/', admin.site.urls),
    url(r'^user_profile/', get_user_profile),
    url(r'^recommendations/', recommendations, name='recommendations'),
    url(r'^entity_search/(?P<entityslug>[-\w]+)$', entity_search, name='entity_search'),
    url(r'^paragraph_search/(?P<paragraphslug>[-\w]+)$', paragraph_search, name='paragraph_search'),
    url(r'^(?P<id>[^/]+)/(?P<slug>[-\w]+)$', DocumentDetailView.as_view(), name='document-detail'),
    url(r'^login/$', login,
        {'template_name': 'document_manager/login.html'},
        name='legal_mining_login'),
    url(r'^logout/$', logout,
        {'next_page': reverse_lazy('legal_mining_login')},
        name='legal_mining_logout'),
    url(r'^$', login_required(SearchView(
        template='search/search.html',
        searchqueryset=sqs,
        form_class=CustomSearchForm
    )), name='haystack_search'),
]
