import logging

from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

from django.db.models import Model


logger = logging.getLogger(__name__)


class CreateUpdateAbstractModel(Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Group(CreateUpdateAbstractModel):
    """
    Model representing a group.
    Groups are a simple way to apply permission mechanism on users.
    """
    nsid = models.CharField(max_length=100, help_text="NSID of the group", db_index=True, unique=True)
    name = models.CharField(max_length=100, help_text="Name of the group")
    description = models.TextField(help_text="Description of the group")


class FlickerUser(CreateUpdateAbstractModel):
    """
    Model representing a flicker user.
    A flicker user is a extension to the django auth user with additional properties custom to the project.
    """
    user = models.OneToOneField(
        User, help_text="User related to the flicker user", on_delete=models.CASCADE
    )
    nsid = models.CharField(help_text="NSID of the user", max_length=100, db_index=True, unique=True)
    real_name = models.CharField(help_text="Real name of the user", max_length=100)
    location = models.CharField(help_text="Location of the user", max_length=100)
    path_alias = models.CharField(max_length=100)

    groups = models.ManyToManyField(Group, help_text="Groups this user belongs too")

    @classmethod
    def get_by_user(cls, user):
        cache_key  = "flicker_user_for_user_id_{0}".format(user.id)
        flicker_user = cache.get(cache_key)
        if not flicker_user:
            logger.info("Cache miss while fetching flicker user")
            flicker_user = cls.objects.get(user=user)
            cache.set(cache_key, flicker_user)

        return flicker_user

    def get_group_ids(self):
        return FlickerUser.groups.through.objects.filter(
            flickeruser_id=self.id
        ).values_list("group_id", flat=True).distinct()


class Tag(CreateUpdateAbstractModel):
    """
    Model representing a tag.
    Each photo can have one or more tags associated with it.
    """
    tag_id = models.CharField(help_text="Verbose tag id", max_length=256, unique=True, db_index=True)
    created_by = models.ForeignKey(
        FlickerUser, help_text="Flicker user who created this tag", on_delete=models.CASCADE
    )
    tag_name = models.CharField(help_text="Name of the tab", max_length=50)


class Photo(CreateUpdateAbstractModel):
    """
    Model representing a photo.
    """
    photo_license_choices = (
        ("0", "PUBLIC"),
        ("1", "PRIVATE"),
    )

    nsid = models.CharField(max_length=100, help_text="NSID of the photo", db_index=True, unique=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    uploaded_on = models.DateTimeField(help_text="Datetime at which this picture was uploaded")
    taken_on = models.DateTimeField(help_text="Datetime at which this picture was taken")

    license = models.CharField(max_length=2, choices=photo_license_choices)

    owner = models.ForeignKey(FlickerUser, help_text="Flicker user which owns this photo", on_delete=models.CASCADE)

    title = models.CharField(max_length=1000, help_text="Title of the picture")
    description = models.TextField(help_text="Description of the photo")

    is_favorite = models.BooleanField(help_text="Is this photo marked as favorite?", default=False)
    is_public = models.BooleanField(help_text="Is this photo public?", default=False)
    is_friend = models.BooleanField(help_text="Is this photo friend only?", default=False)
    is_family = models.BooleanField(help_text="Is this photo family only?", default=False)

    views = models.PositiveIntegerField(help_text="Number of views on this photo", default=0)

    can_comment = models.BooleanField(help_text="Can flickr users comment on this picture?", default=True)
    can_add_meta = models.BooleanField(help_text="Can flickr users add meta content for this picture?", default=True)

    can_add_meta_public = models.BooleanField(
        help_text="Can the world  add meta content for this picture?", default=False
    )

    can_download = models.BooleanField(help_text="Can this picture be downloaded?", default=True)
    can_blog = models.BooleanField(help_text="Can this picture be blogged?", default=True)
    can_share = models.BooleanField(help_text="Can this picture be shared?", default=True)

    tags = models.ManyToManyField(Tag, help_text="Tags for this photo")

    media = models.CharField(help_text="Type of the media", max_length=10)

    @classmethod
    def get_by_nsid(cls, nsid):
        cache_key = "photo_for_nsid_{0}".format(nsid)
        photo = cache.get(cache_key)
        if not photo:
            logger.info("Cache miss while fetching photo")
            try:
                photo = cls.objects.get(nsid=nsid)
            except cls.DoesNotExist:
                photo = None
            else:
                cache.set(cache_key, photo)

        return photo


class Comment(CreateUpdateAbstractModel):
    """
    Model representing a comment on a photo.
    """
    photo = models.ForeignKey(
        Photo, help_text="The photo on which the comment was made", on_delete=models.CASCADE
    )
    comment = models.TextField(help_text="Content of the comment")
    commented_by = models.ForeignKey(
        FlickerUser, help_text="Flicker user who made this comment", on_delete=models.CASCADE
    )


class Note(CreateUpdateAbstractModel):
    """
    Model representing a note on a photo
    """
    photo = models.ForeignKey(Photo, help_text="Photo this note belongs too", on_delete=models.CASCADE)
    note = models.TextField(help_text="Content of the note")
    flicker_user = models.ForeignKey(
        FlickerUser, help_text="Flicker user who made this note", on_delete=models.CASCADE
    )
