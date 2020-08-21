from django.contrib.auth import authenticate


def get_user(username, password):
    user = authenticate(username=username, password=password)

    if user is not None:
        return user
    raise InvalidCredentials


def create_user(form):
    if form.is_valid():
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        return user
    raise InvalidCredentials


class InvalidCredentials(Exception):
    pass
