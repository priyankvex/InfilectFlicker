from rest_framework import serializers
from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from photos.models import Group, Photo, FlickerUser, Comment, Note


class FlickerUserGroupListSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    nsid = serializers.SerializerMethodField()
    photos_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ("name", "nsid", "photos_count")

    def get_name(self, obj):
        return obj["group__name"]

    def get_nsid(self, obj):
        return obj["group__nsid"]

    def get_photos_count(self, obj):
        return obj["count"]


class FlickerUserSerializer(ModelSerializer):
    nsid = CharField()
    username = serializers.SerializerMethodField()
    real_name = CharField()
    location = CharField()
    path_alias = CharField()

    class Meta:
        model = FlickerUser
        fields = ("nsid", "username", "real_name", "location", "path_alias")

    def get_username(self, obj):
        return obj.user.username


class GroupPhotosListSerializer(ModelSerializer):
    photo_nsid = CharField(source="nsid")

    class Meta:
        model = Photo
        fields = ("photo_nsid",)


class PhotosListSerializer(ModelSerializer):
    photo_nsid = CharField(source="nsid")
    group_nsid = serializers.SerializerMethodField()
    uploaded_on = serializers.SerializerMethodField()
    taken_on = serializers.SerializerMethodField()
    license = CharField()
    owner = FlickerUserSerializer()

    class Meta:
        model = Photo
        fields = ("photo_nsid", "group_nsid", "uploaded_on", "taken_on", "license", "owner")

    def get_group_nsid(self, obj):
        return obj.group.nsid

    def get_uploaded_on(self, obj):
        return obj.uploaded_on.strftime('%s')

    def get_taken_on(self, obj):
        return obj.taken_on.strftime('%s')


class CommentSerializer(ModelSerializer):

    comment = serializers.CharField()

    class Meta:
        model = Comment
        fields = ("comment",)


class NoteSerializer(ModelSerializer):

    note = serializers.CharField()

    class Meta:
        model = Note
        fields = ("note",)


class TagSerializer(ModelSerializer):

    name = serializers.CharField(source="tag_name")
    authorname = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    id = serializers.CharField(source="tag_id")

    class Meta:
        model = Comment
        fields = ("name", "authorname", "author", "id")

    def get_authorname(self, obj):
        return obj.created_by.user.username

    def get_author(self, obj):
        return obj.created_by.nsid


class PhotoDetailsSerializer(ModelSerializer):
    photo_nsid = CharField(source="nsid")
    group_nsid = serializers.SerializerMethodField()
    uploaded_on = serializers.SerializerMethodField()
    taken_on = serializers.SerializerMethodField()
    license = CharField()
    owner = FlickerUserSerializer()
    comments = CommentSerializer(source="comment_set", many=True)
    notes = NoteSerializer(source="note_set", many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Photo
        fields = (
            "photo_nsid", "group_nsid", "uploaded_on", "taken_on", "license", "owner", "comments",
            "notes", "tags"
        )

    def get_group_nsid(self, obj):
        return obj.group.nsid

    def get_uploaded_on(self, obj):
        return obj.uploaded_on.strftime('%s')

    def get_taken_on(self, obj):
        return obj.taken_on.strftime('%s')
