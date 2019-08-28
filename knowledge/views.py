# Create your views here.
import re

import simplejson as simplejson
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.serializers import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from knowledge.models import Memory, Tag

import pdb;
#from knowledge.models import Memory, Tag


def index(request):
    if request.user.is_authenticated:
        context = {}
        return render(request, 'knowledge/index.html', context)

    else:
        return render(request, "knowledge/login.html")


def show_memory(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("knowledge:login")
    context = {}
    all_memores = Memory.objects.filter(author=request.user).order_by('pub_date')
    memores_and_tags = list()

    if request.method == "GET":

        if len(all_memores) > 10:
            all_memores = all_memores[:10]
            context['offset'] = 10
        else:
            context['offset'] = len(all_memores) #отсутствуют дополнительные элементы

        for memory in all_memores:
            memores_and_tags.append(memory.field_to_list())
        context["memores_and_tags"] = memores_and_tags

        return render(request, 'knowledge/showAllMemores.html', context)

    elif request.method == "POST":
        offset = int(request.POST['offset'])
        if len(all_memores) > offset:
            all_memores = all_memores[offset:offset+10]
            if len(all_memores) - offset > 10:
                offset += 10
            else:
                offset = 0 #len(all_memores) - offset

        for memory in all_memores:
            memores_and_tags.append(memory.field_to_list())
        context["memores_and_tags"] = memores_and_tags
        context["offset"] = offset

        return HttpResponse(context)


def create_memory(request):

    # pdb.set_trace()
    user = request.user
    if not user.is_authenticated:
        return redirect("knowledge:login")
    if request.method == "POST":
        text = str.strip(request.POST["text"])

        if Memory.objects.filter(author=user, memory_text=text):
            context = {"message": text[0:60]}
            return render(request, 'knowledge/create_memory.html', context)

        raw_tags = request.POST["tags"]
        priority = request.POST["priority"]

        tags_string_list = raw_tags.split(",")
        tags_string_list = list(map(str.strip, tags_string_list))

        while "" in tags_string_list:
            tags_string_list.remove("")
        if len(tags_string_list) == 0:
            tags_string_list.append("no tags")
        all_current_user_tags = Tag.objects.filter(author=user)

        memory = Memory.objects.create(author=user, priority=priority, memory_text=text)
        memory.save()

        tags_for_insert_in_memory = []

        for exist_tag in all_current_user_tags:
            if exist_tag.tag_text in tags_string_list:
                tags_string_list.remove(exist_tag.tag_text)
                tags_for_insert_in_memory.append(exist_tag)

        for string_tag in tags_string_list:
            temp_tag = Tag.objects.create(author=user, tag_text=string_tag)
            temp_tag.save()
            tags_for_insert_in_memory.append(temp_tag)

        for tag in tags_for_insert_in_memory:
            memory.tags.add(tag)
            tag.inc_count()
            tag.save()
        if len(text) < 60:
            context = {"message": text}
        else:
            context = {"message": text[0:60]+"..."}
        # return  HttpResponse(context, status=200)
        return render(request, 'knowledge/create_memory.html', context)

    elif request.method == "GET":
        context = {"message": ''}
        return render(request, 'knowledge/create_memory.html', context)


def new_memory(request):
    pass


def signup(request):
    if request.user.is_authenticated:
        return redirect("knowledge:index")
    return render(request, "knowledge/signup.html", {})


def logout_view(request):
    logout(request)
    return redirect("knowledge:login")


def login_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("knowledge:index")
        else:
            return render(request, "knowledge/login.html", {"error": "неверный логин или пароль"})
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect("knowledge:index")

        return render(request, "knowledge/login.html", {"error": ""})


def logger(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("knowledge:index")
        else:
            return render(request, "knowledge/login.html", {"error": "неверный логин или пароль"})
    else:
        return redirect("knowledge:logout",)


def createUser(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, "knowledge/signup.html", context={'error': "user exists"})
        if User.objects.filter(email=email).exists():
            return render(request, "knowledge/signup.html", context={'error': "email exists"})
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect('knowledge:index')


def search(request):
    pass


def convert_text_to_tags(request):
    if request.method == "POST":
        user = request.user
        request_json_data = simplejson.loads(request.body)
        # pdb.set_trace()
        all_words = re.findall('\w+\S*\w+', request_json_data['text'])
        existing_words = request_json_data['existing_tags']#.split(" ")

        for word in existing_words:
            if word in all_words:
                all_words.remove(word)
        res = []
        # pdb.set_trace()
        all_tags = Tag.objects.filter(author=user)
        all_tags_string = []
        for tag in all_tags:
            all_tags_string.append(tag.tag_text)

        for word in all_words:
            if word in all_tags_string:
                res.append((word, all_tags.filter(tag_text=word)[0].get_count()))
            else:
                res.append((word, 0))
    context = {"tags": res}
    return JsonResponse(context, status=200)


def get_single_tag_counter(request, tag_text):
    if request.method == "GET":
        user = request.user
        single_tag = Tag.objects.filter(author=user).filter(tag_text=tag_text)
        # pdb.set_trace()
        if len(single_tag) == 0:
            return HttpResponse("0", status=200)
        return HttpResponse(single_tag[0].get_count(), status=200)


def temp(request):
    pass
    # print(request.POST)
    # # import ipdb; ipdb.set_trace()
    # num = simplejson.loads(request.body)
    # # pdb.set_trace()
    # # tempword = request.POST['num']
    # context = {"word": num["word"]}
    # # context = "asdf :" + num["num"]
    # # context["word"] = request.POST["word"]
    #
    # return JsonResponse(context, status=200)
