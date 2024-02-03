from django.contrib.auth import authenticate

def check_user(username, password):
    user = authenticate(username=username, password=password)

    if user is not None:
        return True
    else:
        return False