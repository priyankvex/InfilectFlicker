import random
import time

from django.contrib.auth.models import User
from django.utils import timezone
from flickrapi import FlickrAPI
from rest_framework.authtoken.models import Token

from photos.models import FlickerUser, Group, Photo, Tag, Comment, Note, FlickerUserGroup


def create_users():

    user1 = User(username="owlcity_1")
    user1.save()
    user1.set_password("test_password")
    user1.save()

    user2 = User(username="owlcity_2")
    user2.save()
    user2.set_password("test_password")
    user2.save()

    user3 = User(username="owlcity_3")
    user3.save()
    user3.set_password("test_password")
    user3.save()

    user4 = User(username="owlcity_4")
    user4.save()
    user4.set_password("test_password")
    user4.save()

    user5 = User(username="owlcity_5")
    user5.save()
    user5.set_password("test_password")
    user5.save()

    return [user1, user2, user3, user4, user5]


def create_toekns_for_users():

    users = User.objects.all()

    for user in users:
        Token.objects.create(user=user)


def create_flicker_uesrs():

    users = User.objects.all()
    flicker_users = []

    char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    for index, user in enumerate(users):
        flicker_users.append(
            FlickerUser(
                user=user,
                nsid=''.join(random.sample(char_set*6, 6)),
                real_name="Owl City {0}".format(index),
                location="Alaska",
                path_alias="owl_city_{0}".format(index)
            )
        )

    FlickerUser.objects.bulk_create(flicker_users)


def create_groups():
    groups = []
    char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    for index in range(5):
        groups.append(
            Group(
                nsid=''.join(random.sample(char_set*6, 6)),
                name="group_{0}".format(index),
                description="Group description {0}".format(index)
            )
        )

    Group.objects.bulk_create(groups)


def add_user_1_to_groups():

    groups = Group.objects.filter(id__lte=3).all()

    flicker_user = FlickerUser.objects.first()

    for group in groups:
        flicker_user.groups.add(group)


def create_photos():
    api_key = "___"
    secret = "___"
    flickr = FlickrAPI(api_key, secret, format='parsed-json')

    photos_list = flickr.groups.pools.getPhotos(group_id="16978849@N00", per_page=150)["photos"]["photo"]

    flicker_users = FlickerUser.objects.all()
    groups = Group.objects.all()

    photos_instances = []

    for photo_item in photos_list:
        print (len(photos_instances))
        photo_id = photo_item["id"]
        photo_details = flickr.photos.getInfo(photo_id=photo_id)["photo"]
        photos_instances.append(
            Photo(
                group=random.choice(groups),
                owner=random.choice(flicker_users),
                nsid=photo_details["id"],
                uploaded_on=timezone.now(),
                taken_on=timezone.now(),
                license=photo_details["license"],
                title=photo_details["title"],
                description=photo_details["description"],
                views=random.randint(100, 10000),
                media=photo_details["media"]
            )
        )

    Photo.objects.bulk_create(photos_instances)


def add_tags_to_photos():

    flicker_users = FlickerUser.objects.all()

    char_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    tags = []
    for i in range(5):
        tags.append(
            Tag(
                tag_id=''.join(random.sample(char_set*6, 6)),
                created_by=random.choice(flicker_users),
                tag_name="Tag_[0]".format(i)
            )
        )

    Tag.objects.bulk_create(tags)

    tags = Tag.objects.all()

    photos = Photo.objects.all()

    for photo in photos:
        photo.tags.add(random.choice(tags))


def add_comments_to_photos():

    flicker_users = FlickerUser.objects.all()

    photos = Photo.objects.all()

    comments = []

    for photo in photos:
        comments.append(
            Comment(
                photo=photo,
                commented_by=random.choice(flicker_users),
                comment="This is a comment"
            )
        )

    Comment.objects.bulk_create(comments)


def add_notes_to_photos():

    flicker_users = FlickerUser.objects.all()

    photos = Photo.objects.all()

    notes = []

    for photo in photos:
        notes.append(
            Note(
                photo=photo,
                flicker_user=random.choice(flicker_users),
                note="This is a note"
            )
        )

    Note.objects.bulk_create(notes)
