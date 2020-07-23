from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import User
from .models import posts
from .models import profile
from .models import likes
import time
from django.core import serializers
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
def index(request):
  
    
    all =posts.objects.all().order_by("-tmt")
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
           shin.append(ch.pid)
    else:
        shin=[]

  
    paginator = Paginator(all, 10) # Show 25 contacts per page.
    pop=[]
    try:
        pop.append(request.session['username'])
    except:
        pop=[]
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/index.html",{"allposts":page_obj,"current1":pop,"shin":shin})
  


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            request.session['username'] = username
            login(request, user)
          
            try:
               ww=profile.objects.get(usrs= request.session['username'])
            except:
               ww=None
            if ww==None   :
               pro=profile()
               pro.usrs=request.session['username']
               pro.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    if request.session.has_key('username'):

       del request.session['username']
    logout(request)
    
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        request.session['username'] = username
        login(request, user)
        
        try:
            ww=profile.objects.get(usrs=request.session['username'])
        except:
            ww=None
        if ww==None:
            pro=profile()
            pro.usrs=request.session['username']
            pro.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
def post(request):
    return render(request,"network/newp.html")
def postcreate(request):
   if request.method =="POST":
    ui=posts()
    ui.usr=request.session["username"]
    ui.txt=request.POST.get('new')
    ts = time.localtime()
  
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    ui.tmt=timestamp
    ui.save()
    all =posts.objects.all().order_by("-tmt")
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
           shin.append(ch.pid)
    else:
        shin=[]

    all =posts.objects.all().order_by("-tmt")
    paginator = Paginator(all, 10) # Show 25 contacts per page.
    pop=[]
    try:
        pop.append(request.session['username'])
    except:
        pop=[]
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/index.html",{"allposts":page_obj,"current1":pop,"shin":shin})
   else:
    all =posts.objects.all().order_by("-tmt")
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
           shin.append(ch.pid)
    else:
        shin=[]
    paginator = Paginator(all, 10) # Show 25 contacts per page.
    pop=[]
    try:
        pop.append(request.session['username'])
    except:
        pop=[]
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,"network/index.html",{"allposts":page_obj,"current1":pop,"shin":shin})

  
def profilepage(request,nam):
    all1=profile.objects.filter(usrs=nam)
    r=0
    r1=0
    for w in all1:
        if w.followers:
           r=r+1
        if w.following:
           r1=r1+1
    try:
        if nam==request.session['username']:
           bool1=False
           huh=False
        else:
           bool1=True
           huh=False
        mv=profile.objects.filter(usrs=nam)
        for m in mv:
           if m.followers==request.session['username']:
              bool1=False
              huh=True
        al1=posts.objects.filter(usr=nam).order_by("-tmt")
        paginator = Paginator(al1, 10) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj1 = paginator.get_page(page_number)
        pop=[]
    
        pop.append(request.session['username'])
        shin=[]
        try:
            chan=likes.objects.filter(by=request.session['username'])
        except:
            chan=None
        if chan is not None:
            for ch in chan:
              shin.append(ch.pid)
        else:
            shin=[]
        return render(request,"network/profile.html",{"ff":r,"shin":shin,"ff1":r1,"nmk":nam,"bool":bool1,"huh":huh,"allposts":page_obj1,"current1":pop})
    except:
        return render(request,"network/error.html")
def follow(request,nam1):
    fol=profile()
    fol.usrs=nam1
    fol.followers=request.session['username']
    fol.save()
    foll=profile()
    foll.usrs=request.session['username']
    foll.following=nam1
    foll.save()
    alll1=profile.objects.filter(usrs=nam1)
    r=0
    r1=0
    for w in alll1:
       if w.followers:
           r=r+1
       if w.following:
           r1=r1+1
  
    if nam1==request.session['username']:
        bool1=False
        huh=False
    else:
        bool1=True
        huh=False
    mv=profile.objects.filter(usrs=nam1)
    for m in mv:
        if m.followers==request.session['username']:
            bool1=False
            huh=True
    al1=posts.objects.filter(usr=nam1).order_by("-tmt")
    pop=[]
    
    pop.append(request.session['username'])
    paginator = Paginator(al1, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj1 = paginator.get_page(page_number)
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
            shin.append(ch.pid)
    else:
        shin=[]
    return render(request,"network/profile.html",{"ff":r,"shin":shin,"ff1":r1,"nmk":nam1,"bool":bool1,"huh":huh,"current1":pop,"allposts":page_obj1})
def unfollow(request,nam2):
    huh=False
    sh=profile.objects.filter(usrs=nam2,followers=request.session['username'])
    sh.delete()
    sh1=profile.objects.filter(following=nam2,usrs=request.session['username'])
    sh1.delete()
    alll1=profile.objects.filter(usrs=nam2)
    r=0
    r1=0
    for w in alll1:
       if w.followers:
           r=r+1
       if w.following:
           r1=r1+1
  
    if nam2==request.session['username']:
        bool1=False
        huh=False
    else:
        bool1=True
        huh=False
    mv=profile.objects.filter(usrs=nam2)
    for m in mv:
        if m.followers==request.session['username']:
            bool1=False
            huh=True
    al1=posts.objects.filter(usr=nam2).order_by("-tmt")
    pop=[]
    
    pop.append(request.session['username'])
    paginator = Paginator(al1, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj1 = paginator.get_page(page_number)
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
            shin.append(ch.pid)
    else:
        shin=[]
    return render(request,"network/profile.html",{"ff":r,"shin":shin,"ff1":r1,"nmk":nam2,"current1":pop,"bool":bool1,"huh":huh,"allposts":page_obj1})
def folpost(request):
    lis=[]
    lis1=[]
    pps=[]
    foloo=profile.objects.filter(usrs=request.session['username'])
    for ty in foloo:
        if ty.following:
            lis.append(ty.following)
    for l in lis:
        pps.append(posts.objects.filter(usr=l))
    for i in pps:
        lis1.extend(i)
    pop=[]
    
    pop.append(request.session['username'])
    
    paginator = Paginator(lis1, 10) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    shin=[]
    try:
        chan=likes.objects.filter(by=request.session['username'])
    except:
        chan=None
    if chan is not None:
        for ch in chan:
            shin.append(ch.pid)
    else:
        shin=[]


    return render(request,"network/folop.html",{"folop":page_obj,"shin":shin,"current1":pop})
@csrf_exempt
def edit(request,id):
    try:
        post = posts.objects.get(id=id)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method=="GET":
        return JsonResponse(post.serialize())
    elif request.method=="PUT":
        data=json.loads(request.body)
        if data.get("usr")==request.user.username:
            if data.get("txt")is not None:
                post.txt=data["txt"]
        else:
            return JsonResponse({"error":"INVALID"},status=404)
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error":"Try GET"},status=404)
@csrf_exempt
def likedby(request,pp,mnk):
    poop=0
    
    try:
        likepost=likes.objects.filter(pid=pp)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method=="GET":
        return JsonResponse([k.serialize1() for k in likepost], safe=False)
    elif request.method=="POST":
        
        lol=likes()
        
        lol.by=request.session['username']
        lol.pid=pp
        lol.save()
        
          
        loll=posts.objects.get(id=pp)
        for o in likepost:
            poop=poop+1
        loll.likes=poop
        loll.save()
        return HttpResponse(status=204)
@csrf_exempt
def unlike(request,pp1,mnk1):
    poop1=0
    
    try:
        likepost1=likes.objects.filter(pid=pp1)
    except:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method=="GET":
        return JsonResponse([k.serialize1() for k in likepost1], safe=False)
    elif request.method=="DELETE":
        lol=likes.objects.filter(pid=pp1,by=mnk1)
        lol.delete()
        
        loll=posts.objects.get(id=pp1)
        if likepost1 is None:
            poop1=0
        else:
            for o in likepost1:
              poop1=poop1+1
        loll.likes=poop1
        loll.save()
        return HttpResponse(status=204)






        
    


