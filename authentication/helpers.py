from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    refresh['firstName'] = user.first_name
    refresh['lastName'] = user.last_name
    refresh['email'] = user.email

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
