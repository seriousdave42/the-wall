from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User
from .models import Post, Comment
from datetime import timedelta, datetime

def wall(request):
    if "user_id" not in request.session:
        logged_in = False
        context = {
            "recent_posts" : Post.objects.all().order_by("-created_at")[:5],
            "logged_in" : logged_in
        }
    else:
        logged_in = True
        context = {
            "recent_posts" : Post.objects.all().order_by("-created_at")[:10],
            "user_id" : request.session["user_id"],
            "first_name" : request.session["first_name"],
            "logged_in" : logged_in
        }
    return render(request, "index.html", context)

def new_post(request):
    errors = Post.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    Post.objects.create(post_text = request.POST["post_text"],
        user = User.objects.get(id = request.session["user_id"]))
    return redirect('/')

def new_comment(request):
    errors = Comment.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    Comment.objects.create(comment_text = request.POST["comment_text"],
        post = Post.objects.get(id = request.POST["post_id"]),
        user = User.objects.get(id = request.session["user_id"]))
    return redirect('/')

def delete_comment(request):
    comment = Comment.objects.get(id=request.POST["comment_id"])
    comment.delete()
    return redirect('/')

def delete_post(request):
    post = Post.objects.get(id=request.POST["post_id"])
    post.delete()
    return redirect('/')




