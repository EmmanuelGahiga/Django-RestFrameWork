from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()


def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    tokens = {"access": str(access), "refresh": str(refresh)}
    return tokens
