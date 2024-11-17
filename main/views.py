from django.shortcuts import render # type: ignore

def home(request):
    return render(request, 'home.html', {'show_footer': True})

# Note:  This isn't used - the built-in django.contrib.auth is used instead
def login_register(request, action):
    if action == 'login':
        title = 'Login'
        is_login = True
    else:
        title = 'Register'
        is_login = False
    return render(
        request, 'login-register.html',
        {'title': title, 'is_login': is_login, 'show_footer': False}
    )
