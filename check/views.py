from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import difflib

def LoginView(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        password = request.POST.get("password")
        
        user = authenticate(request, username = userName, password = password)
        if user is not None:
            login(request, user)
            return redirect('/check')
        else: 
            return render(request, "login.html", {"error": "User Not Found!"})
    
    return render(request, "login.html")

def RegisterView(request):
    if request.method == "POST":
        userName = request.POST.get("userName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Check if a user with the given username already exists
        if User.objects.filter(username=userName).exists():
            return render(request, "register.html", {"unameError": "Username already taken. Please choose a different username."})
        
        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {"emailError": "Email is already registered. Please use a different email."})
        
        # Create and save the new user
        new_user = User.objects.create_user(username=userName, email=email, password=password)
        new_user.save()
        
        return redirect('/')

    return render(request, "register.html")

@login_required(login_url='/')
def CheckPlagiarismView(request): 
    if request.method == 'POST':
        file1 = request.FILES.get('file1')
        file2 = request.FILES.get('file2')
        
        if file1 and file2: 
            text1 = file1.read().decode('utf-8')
            text2 = file2.read().decode('utf-8')
            
            sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
            similarity_percentage = sequence_matcher.ratio()
                
            returnedResult = int(similarity_percentage*100) 
                
            return render(request, 'result.html', {'similarity': returnedResult})
        else: 
           return render(request, 'result.html', {'similarity': "Files Not Found"}) 
    else:
       return render(request, 'check.html') 
   

def LogoutView(request):
    logout(request)
    return redirect("/")
