import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import WelcomePage, LoginForm
from .models import Followers, TargetUsers, LoginData, TargetHashTags, TargetedHashTagUsers
from django.contrib.auth import authenticate, login
from . import getting_user_id
from . import user_followers
from InstagramAPI import InstagramAPI
import json
from django.contrib import messages


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


def retrieve_followers(request):
    context = ''
    #form = WelcomePage(request.GET or None)

    followers_string = ''
    hash_tag_users_string = ''
    celeb_user_name = ''
    hash_tag = ''

    print(request.GET.get('celeb_user_name'))
    print(request.GET)
    # print(form.is_valid())
    #
    # if form.is_valid():
    if request.GET and request.GET['celeb_user_name']:

        celeb_user_name = request.GET['celeb_user_name']
        hash_tag = request.GET['hash_tag']

        add_followers(celeb_user_name)

        queryset = Followers.objects.all()

        followers_string = ''

        for follower in queryset:
            followers_string += follower.uname_id + ', '


            # context = {
            #     'follower_strings': followers_string,
            #     'celeb_user_name': celeb_user_name
            #     }
    elif request.GET and request.GET['hash_tag']:

        add_hash_tag_users(hash_tag)

        queryset = TargetedHashTagUsers.objects.all()

        hash_tag_users_string = ''

        for follower in queryset:
            hash_tag_users_string += follower.user_name + ', '

    # if form.errors:
    #     print(form.errors)

    template_name = 'automation/dashboard.html'
    return render(
        request,
        template_name,
        {'follower_strings': followers_string,
         'celeb_user': celeb_user_name,
         'hash_tag': hash_tag,
         'hash_tag_users_string': hash_tag_users_string
         }
    )


def like_media(request):
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

                    messages.add_message(request, messages.INFO, update)

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
                    messages.add_message(request, messages.INFO, update)
            else:
                api.follow(follower.u_id)
        else:
            continue

    template_name = 'automation/success.html'
    return render(request, template_name, {})


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


def live_likes_hashtags(request):
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
            if i == 4:
                break

        likes_count += 4

        if likes_count > 15:
            break

    template_name = 'automation/live_likes.html'
    return render(request, template_name, {})
