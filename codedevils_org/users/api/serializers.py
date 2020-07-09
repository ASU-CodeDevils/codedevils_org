from rest_framework import serializers

from codedevils_org.users.models import Officer, OfficerPosition, User

USER_EXCLUDE_FIELDS = ("password", "groups", "user_permissions", "is_staff", "is_superuser", "city",
                       "state", "country")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = USER_EXCLUDE_FIELDS
        description = "CodeDevils user"
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "name", "email", "url")
        description = "CodeDevils user with limited number of returned fields"
        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class OfficerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerPosition
        fields = "__all__"
        description = "Officer positions (i.e. President, VP, etc)"


class OfficerSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(many=False, read_only=True)
    position = OfficerPositionSerializer(many=False, read_only=True)

    class Meta:
        model = Officer
        fields = "__all__"
        description = "CodeDevils officers"
