from django.shortcuts import render,redirect,get_object_or_404
from .models import * 
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from .utils import customSendMail,get_or_create_chatRoom
import random


"""
user.object.get(fieldname=value)
when expecting single result 
e.g at login time
usr.objects.get(email=email)
get method return object if not get it return exception

--------------------------------
user.object.filter(city="ahmedabad")
it return querylist and if list is blank is not return exception
user .first() with filter insted of get()

---------------------------------------
user.object.all()
it is similiar like select query in sql
eg instapost.object.all()

"""
def checkLoggin(view_function):
    def wrapper(request,*args,**kwargs):
        if "email" in request.session:
            try:
                uid = InstaUser.objects.get(email = request.session['email'])
                request.uid = uid 
                return view_function(request,*args,**kwargs)
            except InstaUser.DoesNotExist:
                return redirect("login")
        return redirect("login")
    
    return wrapper

def login(request):
    if request.POST:
        email = request.POST['email']
        password =request.POST['password']

        try:
            uid = InstaUser.objects.get(email = email)
            if not check_password(password,uid.password):
                context = {
                    'e_msg' : "Invalid Credentials !"
                }
                return render(request,"myapp/login.html",context)
            else:
                request.session['email'] = email 
                context = { 'uid' : uid }
                print("----------->>> home",uid)
                return redirect("home")

        except:
            context = {
                'e_msg' : "User Not Found !"
            }
            return render(request,"myapp/login.html",context)

    return render(request,'myapp/login.html')

def signup(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST['gender']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if InstaUser.objects.filter(username=username).exists():
            context = {
                'e_msg' : "Username Already exists !"
            }
            return render(request,"myapp/register.html",context)

        elif InstaUser.objects.filter(email = email).exists():
            context = {
                'e_msg' : "Email Already exists !"
            }
            return render(request,"myapp/register.html",context)

        elif password!= confirm_password:
            context = {
                'e_msg': "Password does not match !"
            }
            return render(request,"myapp/register.html",context)

        else:
            if gender == "male":
                img = "images/boy.png"
            elif gender == "female":
                img = "images/girl.png"

            InstaUser.objects.create(
                    username = username,
                    email = email,
                    password = make_password(password),
                    profile_pic = img ,
                    gender = gender
                    )
                    
            return redirect("login")

    return render(request,"myapp/register.html")

@checkLoggin
def home(request):
    uid = request.uid
    # post_all=InstaPost.objects.all().order_by("-created_at")
    my_following=FollowUsers.objects.filter(following=uid).values_list("following_person",flat=True)
    post_all=InstaPost.objects.filter(user__in = list(my_following) + [uid.id]).order_by("-created_at")
    users=list(my_following) +[uid.id]
    all_user=[InstaUser.objects.get(id=i) for i in users if i!= uid.id ]
    story_all=InstaStory.objects.filter(user__in=users,expired_at__gt=timezone.now()).order_by("user","-created_at")

    context={
        'uid':uid,
        "post_all":post_all,
        "story_all":story_all,
        "all_user":all_user
    }

    return render(request,"myapp/home.html",context)

@checkLoggin
def logout(request):
    del request.session['email']
    return redirect("login")

@checkLoggin
def edit_profile(request):
    uid = request.uid 
    if request.POST:
        username = request.POST['username']
        name = request.POST['name']
        bio = request.POST['bio']
        description = request.POST['description']
        website = request.POST['website']

        uid = InstaUser.objects.get(email = request.session['email'])
        uid.username = username
        uid.name = name 
        uid.bio = bio
        uid.description = description
        uid.link = website

        if 'profile_pic' in request.FILES:
            uid.profile_pic = request.FILES['profile_pic']
        
        uid.save()
        return redirect("home")
    return render(request,"myapp/edit_profile.html",{'uid':uid})

@checkLoggin
def create_post(request):
    uid = request.uid 

    if request.POST:
        caption=request.POST['caption']
        location=request.POST['location']
        image=request.FILES['image']
        InstaPost.objects.create(user=uid,image=image,caption=caption,location=location)

        return redirect("home")
    
    
        
    return render(request,"myapp/create_post.html",{'uid':uid})
@checkLoggin
def profile(request):
    uid=request.uid
    user_post=InstaPost.objects.filter(user=uid).order_by("-created_at")
    count_following=FollowUsers.objects.filter(following=uid).count()
    count_follower=FollowUsers.objects.filter(following_person=uid).count()
    post_count=InstaPost.objects.filter(user=uid).count()
    
    context={
        'uid':uid,
        "user_posts":user_post,
        "following_count":count_following,
        "followers_count":count_follower,
        "post_count":post_count
    }
    return render(request,"myapp/profile.html",context)


@checkLoggin
def followers(request):
    uid=request.uid
    following_users=FollowUsers.objects.filter(following_person=uid)
    following_ids=FollowUsers.objects.filter(following_person=uid).values_list("following_id",flat=True)
    follower_ids=FollowUsers.objects.filter(following=uid).values_list("following_person_id",flat=True)
    context={
        "uid":uid ,
        "following_users" : following_users,
        "following_ids": following_ids,
        "follower_ids":follower_ids
    }
    return render(request,"myapp/followers.html",context)

@checkLoggin
def following(request):
    uid=request.uid
    following_users=InstaUser.objects.exclude(id=uid.id)
    following_ids=FollowUsers.objects.filter(following=uid).values_list("following_person_id",flat=True)
    # my_following=FollowUsers.objects.filter(following=uid)
    query=request.GET.get('q')

    if query:
        following_users=following_users.filter(
            Q(username__icontains=query)|
            Q(name__icontains=query)
        )

    context={
        "uid" : uid,
        "following_users": following_users,
        "following_ids":following_ids,
        # "following_ids":my_following

    }
    return render(request,"myapp/following.html",context)

@checkLoggin
def follow_unfollow(request,pk):
    uid=request.uid
    
    target_user=InstaUser.objects.get(id=pk)

    following_persons=FollowUsers.objects.filter(following=uid,
                                                 following_person=target_user).first()
    
    if following_persons:
        following_persons.delete()
    else:
        FollowUsers.objects.create(following=uid,
                                   following_person=target_user)
        Notifications.objects.create(sender=uid,
                                     receiver=target_user,
                                     message="Started Following ",
                                     notification_type="follow")
        

    return redirect("following")

@checkLoggin
def remove_follower(request,pk):
    uid=request.uid
    target_user=InstaUser.objects.get(id=pk)

    folowing_user=FollowUsers.objects.filter(following=target_user,following_person=uid).first()
    folowing_user.delete()

    
    return redirect("followers")

@checkLoggin
def follow_back(request,pk):
    uid=request.uid
    
    target_user=InstaUser.objects.get(id=pk)

    following_persons=FollowUsers.objects.filter(following=uid,
                                                 following_person=target_user).first()
    
    if following_persons:
        following_persons.delete()
    else:
        FollowUsers.objects.create(following=uid,
                                   following_person=target_user)
        

    return redirect("followers")


@checkLoggin
def notifications(request):
    uid=request.uid
    all_notifications=Notifications.objects.filter(receiver=uid)
    my_following=FollowUsers.objects.filter(following=uid).values_list("following_person",flat=True)

    context={
        "uid":uid,
        "all_notifications":all_notifications,
        "my_following":my_following

    }
    return render(request,"myapp/notifications.html",context)

@checkLoggin
def like_unlike(request,pk):
    uid=request.uid
    post_id=InstaPost.objects.get(id=pk)
    likes=Like_Unlike.objects.filter(user_fk=uid,post_fk=post_id).first()
    if likes:
        likes.delete()
    else:
        Like_Unlike.objects.create(user_fk=uid,post_fk=post_id)
        if post_id.user !=uid:
            Notifications.objects.create(sender=uid,
                                        receiver=post_id.user,
                                        notification_type="like",
                                        post_fk=post_id,
                                        message="liked your post")
            

    return redirect("home")

@checkLoggin
def create_reels(request):
    uid=request.uid
    if request.POST:
        video=request.FILES['video']
        caption=request.POST.get('caption')

        InstaReels.objects.create(user=uid,video=video,caption=caption)
    context={
        'uid':uid
    }
    return render(request,"myapp/create_reels.html",context)

@checkLoggin
def reels(request):
    uid=request.uid
    post_all=InstaReels.objects.all().order_by("-created_at")

    context={
        'uid':uid,
        "post_all":post_all
    }
    return render(request,"myapp/reels.html",context)


@checkLoggin
def create_story(request):
    uid=request.uid
    if request.POST:
        image=request.FILES['image']
        caption=request.POST['caption']
        story_text=request.POST['story_text']
        istory=InstaStory.objects.create(
            user=uid,
            image=image,
            caption=caption,
            story_text=story_text
        )
        
        if "music"  in request.FILES:
            istory.music=request.FILES['music']
        istory.save()
    context={
        'uid':uid
    }
    return render(request,"myapp/create_story.html",context)

def forgot_password(request):
    if request.POST:
        email=request.POST['email']
        try:
            user=InstaUser.objects.get(email=email)
            if user:
                otp=random.randint(1111,9999)
                user.otp=otp
                user.save()
                customSendMail("Forgot Password","mail_template",email,{'otp':otp})
                context={
                    'email':email
                    
                }
                return render(request,"myapp/otp.html",context)
        except:
            context={
                "e_msg":"User not Found"
            }
            return render(request,"myapp/forgot_password.html",context)
       
    else:
        return render(request,"myapp/forgot_password.html")

def reset_password(request):
    if request.POST:
        email=request.POST['email']
        new_password=request.POST['New Password']
        re_password=request.POST['Confirm Password']
        uid=InstaUser.objects.get(email=email)
        if new_password==re_password:
            uid.password=make_password(new_password)
            uid.save()
            return redirect('login')
        else:
            
         return render(request,"myapp/reset_password.html",{'e_msg':"password not match"})

        
            
    return render(request,"myapp/reset_password.html")

def otp(request):
    if request.POST:
        email=request.POST['email']
        otp_f=request.POST['OTP']
        uid=InstaUser.objects.get(email=email)

        if str(uid.otp)==str(otp_f):

            return render(request,"myapp/reset_password.html",{'email':email})

        else:
            return render(request,"myapp/forgot_password.html",{"e_msg":"invalid otp"})
    return render(request,"myapp/otp.html")


@checkLoggin
def chat_screen(request, pk=None):
    uid = request.uid
    sender = InstaUser.objects.get(id=uid.id)
    receiver = None

    # Get following users
    following_list = FollowUsers.objects.filter(following=sender)
    following_users = [follow.following_person for follow in following_list]

    messages = None  # default

    if pk:
        receiver = InstaUser.objects.get(id=pk)
        conversation_room = get_or_create_chatRoom(sender, receiver)
        messages = Message.objects.filter(chat_room=conversation_room)

    context = {
        'uid': uid,
        'sender': sender,
        "following_users": following_users,
        "receiver": receiver,
        "messages": messages
    }

    return render(request, "myapp/chat_screen.html", context)
@checkLoggin
def send_message(request, pk):

    if request.method == "POST":

        uid = request.uid

        sender = InstaUser.objects.get(id=uid.id)
        receiver = InstaUser.objects.get(id=pk)

        conversation_room = get_or_create_chatRoom(sender, receiver)

        text_message = request.POST.get('message_text')

        msg_obj = Message.objects.create(
            chat_room=conversation_room,
            sender_id=sender,
            text_message=text_message
        )

        # IMAGE
        image = request.FILES.get('image')

        if image:
            msg_obj.image = image

        # VIDEO
        video = request.FILES.get('video')

        if video:
            msg_obj.video = video

        msg_obj.save()

        return redirect("chat_screen", pk=receiver.id)
                  
@checkLoggin
def story_viewer(request, user_id):
    uid = request.uid

    # Step 1: Get users that current user can see (following + self)
    following_ids = FollowUsers.objects.filter(
        following=uid
    ).values_list("following_person", flat=True)

    users_with_stories = list(following_ids) + [uid.id]

    # Step 2: Get all users who currently have active stories
    users_list = InstaUser.objects.filter(
        id__in=InstaStory.objects.filter(
            user__in=users_with_stories,
            expired_at__gt=timezone.now()
        ).values_list('user_id', flat=True).distinct()
    )

    users_ids = list(users_list.values_list('id', flat=True))

    # Step 3: Current user (whose story is being viewed)
    current_user = get_object_or_404(InstaUser, id=user_id)

    # Step 4: Get all active stories of this user
    stories = list(
        InstaStory.objects.filter(
            user=current_user,
            expired_at__gt=timezone.now()
        ).order_by('created_at')
    )

    # Step 5: Get story index from query param
    try:
        story_index = int(request.GET.get('s', 0))
    except:
        story_index = 0

    # Step 6: Handle invalid cases
    if not stories:
        # No stories → move to next user
        if current_user.id in users_ids:
            idx = users_ids.index(current_user.id)
            if idx < len(users_ids) - 1:
                next_user = users_ids[idx + 1]
                return redirect(f"/story/{next_user}/?s=0")
        return redirect("/")  # fallback to home

    if story_index >= len(stories):
        story_index = 0

    # Step 7: Get current story
    current_story = stories[story_index]

    # Step 8: Next / Previous story (same user)
    next_story_index = story_index + 1 if story_index < len(stories) - 1 else None
    prev_story_index = story_index - 1 if story_index > 0 else None

    # Step 9: Next / Previous user
    if current_user.id in users_ids:
        user_idx = users_ids.index(current_user.id)

        next_user = users_ids[user_idx + 1] if user_idx < len(users_ids) - 1 else None
        prev_user = users_ids[user_idx - 1] if user_idx > 0 else None
    else:
        next_user = None
        prev_user = None

    # Step 10: Context
    context = {
        "uid": uid,
        "current_user": current_user,
        "story": current_story,  # 🔥 ONLY ONE STORY
        "story_index": story_index,
        "next_story_index": next_story_index,
        "prev_story_index": prev_story_index,
        "next_user": next_user,
        "prev_user": prev_user,
    }
    

    return render(request, "myapp/story_viewer.html", context)

