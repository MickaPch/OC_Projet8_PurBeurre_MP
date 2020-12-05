from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class AuthenticateBackend(ModelBackend):
    """Authenticate User by email OR username"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Try authenticate by login (username or email)"""

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
            print('Mail exists', user)
        except UserModel.DoesNotExist:
            print('Login not corresponding to email')
            try:
                user = UserModel.objects.get(username=username)
                print('Username exists', user)
            except UserModel.DoesNotExist:
                return None
            else:
                print('Password check for user authenticate by username...')
                if user.check_password(password):
                    print('User verified', user)
                    return user
        else:
            print('Password check for user authenticate by email...')
            if user.check_password(password):
                print('User verified', user)
                return user
        
        return None
