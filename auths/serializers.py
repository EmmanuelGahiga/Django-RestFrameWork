from rest_framework import serializers
from .models import UserModel
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = "__all__"

    # Verify that the email exists
    def validate(self, attrs):
        email_exists = UserModel.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Sorry, the Email has been used")

        return super().validate(attrs)

    # Hash/Crypt the password
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return user


# SERIALIZER FOR RELATIONS MODELS
class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="details_modify_delete_post",
        read_only=True,
    )

    class Meta:
        model = UserModel
        fields = ["id", "username", "email", "posts"]
