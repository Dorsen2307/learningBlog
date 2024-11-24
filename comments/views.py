from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .models import Comment
from .forms import CommentForm
