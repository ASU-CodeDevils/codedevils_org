from rest_framework import serializers

from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail


class BlacklistDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistDomain
        fields = "__all__"


class BlacklistEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistDomain
        fields = "__all__"
