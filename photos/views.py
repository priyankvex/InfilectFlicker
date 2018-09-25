from django.db.models import Count
# Create your views here.
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.versioning import URLPathVersioning

from photos.models import FlickerUser, Photo
from photos.permissions import ValidGroup, ValidPhoto
from photos.serializers import FlickerUserGroupListSerializer, GroupPhotosListSerializer, PhotosListSerializer, \
    PhotoDetailsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class FlickerUserGroupListView(ListAPIView):
    """
    View to fetch all the groups that the user belongs to.
    URL: /api/v1/groups/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = FlickerUserGroupListSerializer
    versioning_class = URLPathVersioning
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        flicker_user = FlickerUser.get_by_user(self.request.user)
        groups = flicker_user.get_group_ids()

        return Photo.objects.filter(
            group_id__in=groups
        ).values("group__name", "group__nsid").annotate(count=Count("id"))


class GroupPhotosListView(ListAPIView):
    """
    View to fetch all the photos for a given group.
    URL: api/v1/groups/<group_nsid>/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ValidGroup]
    serializer_class = GroupPhotosListSerializer
    versioning_class = URLPathVersioning
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_nsid = self.kwargs["group_nsid"]
        return Photo.objects.filter(group__nsid=group_nsid).only("id")


class PhotosListView(ListAPIView):
    """
    View to list photos of a given group.
    URL: api/v1/photos/?group=<group_nsid>/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ValidGroup]
    serializer_class = PhotosListSerializer
    versioning_class = URLPathVersioning
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_nsid = self.request.GET["group"]
        return Photo.objects.filter(group__nsid=group_nsid).select_related("owner", "group", "owner__user")


class PhotoDetailsView(RetrieveAPIView):
    """
    View to fetch photo details for a given photo
    URL: api/v1/photos/<photo_nsid>/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ValidPhoto]
    serializer_class = PhotoDetailsSerializer
    versioning_class = URLPathVersioning
    lookup_url_kwarg = "photo_nsid"

    def get_object(self):
        nsid = self.kwargs["photo_nsid"]
        return Photo.objects.select_related("owner", "group", "owner__user").prefetch_related(
            "comment_set", "tags__created_by__user", "note_set"
        ).get(nsid=nsid)


class LogoutView(CreateAPIView):
    """
    View to delete authentication token for a user
    URL: api/v1/logout/
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        Token.objects.filter(user=user).delete()
        return HttpResponse(status=status.HTTP_200_OK)
