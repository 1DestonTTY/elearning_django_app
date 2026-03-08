from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import UserRegistrationForm
from .models import Student, Teacher, User

#---------register view-------------
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES) #request.FILES is for photo
        if form.is_valid():
            #save new user
            user = form.save()
            
            #create the profile based on the chosen role
            if user.is_student:
                Student.objects.create(user=user)
            elif user.is_teacher:
                Teacher.objects.create(user=user)
                
            return redirect('login') #redirect to login
    else:
        form = UserRegistrationForm()
    
    #render the register page
    return render(request, 'accounts/registerpage.html', {'form': form})

#-----------home view------------
@login_required
def home(request):
    #if user type a new status and click submit
    if request.method == 'POST':
        new_status = request.POST.get('status_text') #grab the text from the form
        if new_status is not None:
            request.user.status_update = new_status 
            request.user.save() #save the status                 
        return redirect('home') 
        
    #render the home page
    return render(request, 'accounts/homepage.html')

#-----------user search------------
@login_required
def user_search(request):
    #only teacher is allow access
    if not request.user.is_teacher:
        return redirect('home')
    
    #get the search term from the URL
    query = request.GET.get('q', '') 
    
    #hide admin and the person making the search
    users_list = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    
    #search the database
    if query:
        users_list = users_list.filter(
            Q(real_name__icontains=query) | Q(username__icontains=query)
        )

    #limit to 10 users per page
    paginator = Paginator(users_list, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/user_search.html', {'users': page_obj, 'query': query})
