from django.shortcuts import render, redirect
import bcrypt
from .models import User, Message, Comment
from django.contrib import messages

def index(request):
    if "user_id" in request.session: #so if a logged in user leaves it will redirect them to the wall, until they click logout
        return redirect('/wall')
    return render(request, "wall_app/index.html")

#Register new user
def register(request):
    errors = User.objects.register_validator(request.POST) #using validation to make sure user meets registration requirements
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        pwhash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()) #hashing the password with bcrypt
        new_user = User.objects.create(first_name=request.POST["fname"], last_name=request.POST["lname"], email=request.POST["email"], pw=pwhash) #creating the new user
        request.session["user_id"] = new_user.id #storing the user session id
        return redirect("/wall")

#Login
def login(request): #Validate to make sure the email is registered
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wall")
    else:
        user = User.objects.filter(email=request.POST['email'])  #Checking to see that login email is in the DB
        if user: 
            logged_user = user[0] #starting from the first index
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.pw.encode()): #checking to see that user login pw is the same one associated with email
                request.session['user_id'] = logged_user.id #storing user ID in session once the PW & Email match DB
                return redirect('/wall')
        return redirect("/") 

#Successful registration and redirect to main page
def wall(request):
    if "user_id" not in request.session: #if the session ID can't be found in session
        messages.error(request, "Not logged in")
        return redirect("/")
    else:
        user = User.objects.get(id=request.session["user_id"]) #store session user ID in context
        all_messages = Message.objects.all() #store messages to display on page
        all_comments = Comment.objects.all()
        context = {
            "user_id": user,
            "all_messages": all_messages,
            "all_comments": all_comments
        }
        return render(request, "wall_app/wall.html", context)

#Message
def post_message(request):
    Message.objects.create(message=request.POST['message'],user=User.objects.get(id=request.session['user_id']))
    return redirect('/wall')

#Post Comment
def post_comment(request):
    Comment.objects.create(message=Message.objects.get(id=request.POST['msgID']),user=User.objects.get(id=request.session['user_id']),comment=request.POST['comment'])
    return redirect('/wall')    

#Delete Message
def delete_message(request, num):
        user = request.session['user_id']
        if user:
            m = Message.objects.get(id = num)
            m.delete()
            return redirect('/wall')
        return redirect("/")

#Logout
def logout(request):
    request.session.clear()
    return redirect("/")


