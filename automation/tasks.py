# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import getting_user_id
from .models import LoginData, Followers, TargetUsers
from django.contrib import messages
from InstagramAPI import InstagramAPI


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def my_name(name):
    name = name + " The Great"
    return name


@shared_task
def like_and_follow():

    login_obj = LoginData.objects.all().first()
    username = login_obj.username
    password = login_obj.password
    api = InstagramAPI(username, password)

    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        print(api.LastJson)  # print last response JSON
        print("Login succes!")
    else:
        print("Can't login!")

    target_user_obj = TargetUsers.objects.all().first()

    queryset = Followers.objects.filter(targetusers=target_user_obj)

    likes_count = 0
    count = 0
    for follower in queryset:
        count += 1
        if count % 5 == 0:

            if follower.is_public:
                try:
                    api.getTotalUserFeed(follower.u_id)

                    update = follower.uname_id + " \'s " + "recent posts have been liked"

                    #messages.add_message(request, messages.INFO, update)

                    i = 0
                    for user in api.getTotalUserFeed(follower.u_id):
                        api.like(user['id'])
                        i += 1
                        if i == 4:
                            break

                    likes_count += 4

                    if likes_count > 17:
                        break

                except:

                    update = "Can't like " + follower.uname_id + " \'s photos"
                    #messages.add_message(request, messages.INFO, update)
            else:
                api.follow(follower.u_id)
        else:
            continue


