from rest_framework import serializers

from codedevils_org.users.models import User, Officer, OfficerPosition


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class OfficerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficerPosition
        fields = "__all__"
        description = "Officer positions (i.e. President, VP, etc)"


class OfficerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Officer
        fields = "__all__"
        description = "The students holding the officer positions"
