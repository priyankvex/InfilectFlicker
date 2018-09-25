from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from photos.models import FlickerUser, Photo


class ValidGroup(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if the given group nsid is valid for the user or not
        """
        flicker_user = FlickerUser.get_by_user(request.user)
        group_nsid = request.resolver_match.kwargs.get("group_nsid")

        if not group_nsid:
            group_nsid = request.GET.get("group")

        if not group_nsid:
            return True

        try:
            FlickerUser.groups.through.objects.get(
                flickeruser_id=flicker_user.id, group__nsid=group_nsid
            )
        except ObjectDoesNotExist:
            has_perm = False
        else:
            has_perm = True

        return has_perm


class ValidPhoto(BasePermission):
    def has_permission(self, request, view):
        """
        Checks if the given photo nsid is valid for the user or not
        """
        flicker_user = FlickerUser.get_by_user(request.user)
        photo_nsid = request.resolver_match.kwargs.get("photo_nsid")

        photo = Photo.get_by_nsid(photo_nsid)

        if not photo:
            return False

        photo_group_id = photo.group_id

        try:
            FlickerUser.groups.through.objects.get(
                flickeruser_id=flicker_user.id, group_id=photo_group_id
            )
        except ObjectDoesNotExist:
            has_perm = False
        else:
            has_perm = True

        return has_perm
