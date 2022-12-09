from django.shortcuts import render
from coupark.forms import UserProfileInfoForm, UserForm
from coupark.models import ParkingSpace, ParkingReservation, Date

# For login:
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index( request ):

    lastDate = Date.objects.last()
    availableSpaces = ParkingReservation.objects.filter( date = lastDate )
    currentUserReservation = True if ParkingReservation.objects.filter( date = lastDate, user = request.user ) else False

    return render( request, 'coupark/index.html', {'spaces': availableSpaces, 'dateBooking': lastDate, 'hasReservation': currentUserReservation} )

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def reservations(request):
    lastDate = Date.objects.last()
    currentUserReservations = ParkingReservation.objects.filter( user = request.user )

    return render( request, 'coupark/reservations.html', { 'currentUserReservations': currentUserReservations, 'dateBooking': lastDate} )

@login_required
def reserve(request, pk):
    #Handles reservation 
    
    lastDate = Date.objects.last()
    availableSpaces = ParkingReservation.objects.filter( date = lastDate )
    currentUserReservation = ParkingReservation.objects.filter( date = lastDate, user = request.user )

    if len(currentUserReservation) > 0 and currentUserReservation.get(id = pk) != None:
        ParkingReservation.objects.update_or_create(id = pk, defaults={'user':None})
        return HttpResponseRedirect(reverse('index'))

    if availableSpaces.filter( id = pk ) != None and len(currentUserReservation) == 0:
        ParkingReservation.objects.update_or_create(id = pk, defaults={'user':request.user})
        return HttpResponseRedirect(reverse('index'))
    

def register( request ):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save( commit = False )
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

            # Login registered users.

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate( username=username, password=password )

            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('Account not active')
            else:
                print('Someone tried to log in and failed')
                print( f'Username {username} and Password {password}' )
                return HttpResponse( 'Invalid login details supplied!' )

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render( request, 'coupark/registration.html', {'registered': registered, 'user_form': user_form, 'profile_form': profile_form} )


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate( username=username, password=password )

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('Someone tried to log in and failed')
            print( f'Username {username} and Password {password}' )
            return HttpResponse( 'Invalid login details supplied!' )
    else:
        return render( request, 'coupark/login.html', {} )