from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import WelcomePage, LoginForm
from .models import (Followers,
                     TargetUsers,
                     LoginData,
                     TargetHashTags,
                     TargetedHashTagUsers,
                     UserConfigurationsState)
from django.contrib.auth import authenticate, login
from . import getting_user_id
from . import user_followers
from InstagramAPI import InstagramAPI
import json
from django.contrib import messages
from django.http import HttpResponse


def add_followers(celeb_user_name):

    queryset = LoginData.objects.all().first()

    username = queryset.username
    password = queryset.password
    print(celeb_user_name)
    target_user = TargetUsers(users=celeb_user_name, login_user=queryset)
    target_user.save()

    print(target_user)

    u_id = getting_user_id.used_id_from_username(
        celeb_user_name,
        username,
        password)

    api = InstagramAPI(username, password)
    api.login()

    # maxid = ''
    # has_more_value = True
    #
    # while has_more_value:
    #     #print("Hey I am here!")
    #     api.getUserFollowers(u_id, maxid)  # (userid,maxid)
    #     for i in api.LastJson['users']:
    #         is_private = i['is_private']
    #         pk = i['pk']
    #         username = i['username']
    #         print(username)
    #
    #         Followers.objects.create(
    #             targetusers=target_user,
    #             uname_id=username,
    #             u_id=pk,
    #             is_public=not is_private)
    #         #followerlist.append(i['pk'])
    #     if not api.LastJson['big_list']:
    #         break
    #     maxid = api.LastJson['next_max_id']
    #     time.sleep(1)

    followers = user_followers.getTotalFollowers(api, u_id)

    for follower in followers:
        is_private = follower['is_private']
        pk = follower['pk']
        username = follower['username']
        Followers.objects.create(
            targetusers=target_user,
            uname_id=username,
            u_id=pk,
            is_public= not is_private)


def login_view(request):
    form = LoginForm(data=request.POST)

    if form.is_valid():
        user_obj = form.cleaned_data
        user_name = user_obj['Username']
        password = user_obj['Password']

        LoginData.objects.create(username=user_name, password=password)

    if form.errors:
        print(form.errors)
    else:
        return HttpResponseRedirect('/automation/welcome/')
    template_name = 'automation/index.html'
    context = {}
    return render(request, template_name, context)


def like_media(likes_per_hour):

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

    for follower in queryset:
            likes_count = 0
            if follower.is_public and not follower.is_processed:
                api.getTotalUserFeed(follower.u_id)
                i = 0
                for user in api.getTotalUserFeed(follower.u_id):
                    print(follower.u_id + ' \s ' + user['id'] + " is liked")
                    #api.like(user['id'])
                    follower.is_processed = True
                    follower.save(update_fields=["is_processed"])

                    i += 1
                    likes_count += 1
                    if i > 4:
                        break
            else:
                api.follow(follower.u_id)

            if likes_count > 4:
                break

def add_hash_tag_users(hash_tag):
    login_obj = LoginData.objects.all().first()

    username = login_obj.username
    password = login_obj.password

    tags = TargetHashTags(htags=hash_tag, login_user=login_obj)
    tags.save()

    api = InstagramAPI(username, password)

    if (api.login()):
        api.getSelfUserFeed()  # get self user feed
        print(api.LastJson)  # print last response JSON
        print("Login succes!")
    else:
        print("Can't login!")

    api.getHashtagFeed(hash_tag)

    user_ids = []

    response = api.LastJson

    with open('hashtags_feed.txt', 'w') as outfile:
        json.dump(response, outfile)

    with open('hashtags_feed.txt') as json_data:
        d = json.load(json_data)

        for x in d['ranked_items']:
            for keys in x:
                if keys == 'user':
                    user_ids.append(x['user']['username'])

    queryset = TargetHashTags.objects.all().first()

    for user in user_ids:
        TargetedHashTagUsers.objects.create(targethashtags=tags, user_name=user)


def live_likes_hashtags(likes_per_hour):
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

    queryset = TargetedHashTagUsers.objects.all()

    likes_count = 0

    for follower in queryset:

        print(follower.user_name)

        u_id = getting_user_id.used_id_from_username(follower.user_name, username, password)

        api.getTotalUserFeed(u_id)
        i = 0
        for user in api.getTotalUserFeed(u_id):
            api.like(user['id'])
            i += 1
            likes_count += 1
            if i > 3:
                break

        if likes_count > likes_per_hour:
            break


def calling_actions():
    queryset = UserConfigurationsState.objects.all()
    celeb_user_names = ''
    hash_tags = ''
    likes_per_hour = ''

    for item in queryset:
        celeb_user_names = item.celeb_user_name
        hash_tags = item.hash_tag
        likes_per_hour = item.likes_per_hour

    add_followers(celeb_user_names)

    add_hash_tag_users(hash_tags)

    like_media(int(likes_per_hour))

    return None


def user_preferences(request):

    if len(request.GET) > 0:

        celeb_user_names = request.GET.get('celeb_user_name')
        hash_tags = request.GET.get('hash_tag')
        likes_per_hour = request.GET.get('likes_per_hour')
        print(request.GET.get('from_date'))
        from_date = datetime.strptime(request.GET.get('from_date'), '%m/%d/%Y')
        to_date = datetime.strptime(request.GET.get('to_date'), '%m/%d/%Y')

        UserConfigurationsState.objects.create(celeb_user_name=celeb_user_names,
                                               hash_tag=hash_tags,
                                               likes_per_hour=likes_per_hour,
                                               from_date=from_date,
                                               to_date=to_date)
        calling_actions()

    template_name = 'automation/dashboard.html'
    return render(request, template_name)


