from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Student_card, Activity
# Create your views here.
def index(request):
    activity = Activity.objects.all()
    return render(request, 'fp10_app/index.html', {"activity": activity})

@login_required
def join_activity(request, activity_id):
    print("fp")
    
    activity = get_object_or_404(Activity, id=activity_id)
    if request.user not in activity.partitions.all():
        activity.partitions.add(request.user)
    activity = Activity.objects.all()
    return render(request, 'fp10_app/index.html', {"activity": activity})

def create_activity(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        picture = request.FILES.get('picture')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        
        activity = Activity(
            title=title,
            text=text,
            picture=picture,
            owner=request.user,  
            start_time=start_time,
            end_time=end_time
        )
        activity.save()

        return redirect('/')  
    return render(request, 'fp10_app/index.html', {"activity": activity})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.POST:
        username = request.POST['username']
        try:
            user = CustomUser.objects.get(username=username)
        except:
            user = None
        if user is None:
            return render(request, 'registration/login.html', {'error_message': 'Böyle bir kullanıcı yok.'})
        password = request.POST['password']
        next_url = request.POST.get('next')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            auth_login(request, user)
            if next_url:  
                return redirect(next_url)
            else:
                return redirect('/')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Yanlış şifre.'})
    return render(request, 'registration/login.html')

def signup_view(request):
    error_messages = {}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            print(form.errors)
            if 'username' in form.errors:
                error_messages['username_error'] = 'Bu kullanıcı adı zaten kullanılıyor. Lütfen farklı bir kullanıcı adı seçin.'
            
            if 'email' in form.errors:
                error_messages['email_error'] = 'Bu e-posta adresi zaten kullanılıyor. Lütfen farklı bir e-posta adresi seçin.'

            if 'password1' in form.errors or 'password2' in form.errors:
                error_messages['password_error'] = 'Girdiğiniz şifreler eşleşmiyor veya şifre yeterliliklerini karşılamıyor. Lütfen şifrenizi kontrol edin.'

            if 'username' not in form.data:
                error_messages['username_missing'] = 'Kullanıcı adı alanı boş bırakılamaz.'
            
            if 'email' not in form.data:
                error_messages['email_missing'] = 'E-posta alanı boş bırakılamaz.'

    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form, 'error_messages': error_messages})


def student_card_verification(request):
    if request.method == "POST":
        image = request.FILES.get("student-card-photo")
        Student_card.objects.create(student_card=image, student_owner=request.user)
        return redirect('/')
