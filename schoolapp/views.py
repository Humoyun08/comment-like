from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import json
# Create your views here.
def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, 'blog_index.html', {'posts': posts})

def blog_detail(request, slug):
    post = Post.objects.get(slug = slug)
    
    comments = post.comments.all()
    new_comment = None
    form = CommentForm()
    msg = False
    
    if request.user.is_authenticated:
        user = request.user
        
    
        if post.likes.filter(id=user.id).exists():
            msg = True
    
    
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    return render(request, 'blog_detail.html',{'post': post, 'comments':comments,'form':form, 'new_comment': new_comment, 'msg':msg})




def replyComment(request, slug):
    commment = Comment.objects.get(slug = slug)
    reply = commment.reply_comments.all()
    new_repyl_comment = None
    forms = ReplyCommentForm()
    m = False
    if request.method == 'POST':
        forms = ReplyCommentForm(request.POST)
        if forms.is_valid():
            new_repyl_comment = forms.save(commit=False)
            new_repyl_comment.commment = commment
            new_repyl_comment.save()
    return render(request, 'reply.html',{'reply':reply,'m':m,})
    


    
    
def like_post(request):

    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = None
    
    if request.user.is_authenticated:
        
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0
            
            
        else:
            post.likes.add(request.user)
            checker = 1
    
    likes = post.likes.count()
    
    info = {
        "check": checker,
        "num_of_likes": likes
    }
    
    return JsonResponse(info, safe=False)


