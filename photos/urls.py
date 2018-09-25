from django.conf.urls import url

from photos.views import FlickerUserGroupListView, GroupPhotosListView, PhotosListView, PhotoDetailsView, LogoutView

urlpatterns = [
    url(r'api/(?P<version>(v1))/groups/$', FlickerUserGroupListView.as_view(), name="groups_list"),
    url(
        r'api/(?P<version>(v1))/groups/(?P<group_nsid>[a-zA-Z0-9]+)/$',
        GroupPhotosListView.as_view(), name="groups_photos_list"
    ),
    url(r'api/(?P<version>(v1))/photos/$', PhotosListView.as_view(), name="photos_list"),
    url(
        r'api/(?P<version>(v1))/photos/(?P<photo_nsid>[a-zA-Z0-9]+)/$', PhotoDetailsView.as_view(),
        name="photos_details"
    ),
    url(r'api/(?P<version>(v1))/logout/$', LogoutView.as_view(), name="logout"),
]
