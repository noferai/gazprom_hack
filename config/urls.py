from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views import defaults as default_views

from rest_framework.routers import DefaultRouter

from tdmt.tenders import views as tenders_views
from tdmt.users import views as user_views

router = DefaultRouter()
router.register(r"tasks", tenders_views.TaskViewSet)
router.register(r"staff", user_views.UserViewSet)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    url(r"^login/$", auth_views.LoginView.as_view(), name="login"),
    url(r"^logout/$", auth_views.LogoutView.as_view(), {"next_page": "/"}, name="logout"),
    # comments app
    url(r"^comments/", include("django_comments_xtd.urls")),
    # API urls
    url(r"^api/", include(router.urls)),
    # User management
    url(r"^staff/", include("tdmt.users.urls")),
    # Tenders
    path(r"", include("tdmt.tenders.urls", namespace="tenders")),
    url(r"^tinymce/", include("tinymce.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    import debug_toolbar

    urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls)),] + urlpatterns  # prepend

    urlpatterns += [
        url(r"^400/$", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
        url(r"^403/$", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
        url(r"^404/$", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        url(r"^500/$", default_views.server_error),
    ]
