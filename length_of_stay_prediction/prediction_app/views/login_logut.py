from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def user_login(request):

    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return HttpResponseRedirect(reverse('home'))
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html')
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))