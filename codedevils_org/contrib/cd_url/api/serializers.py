from rest_framework import serializers

from codedevils_org.contrib.cd_url.models import CustomUrl


class CustomUrlSerializer(serializers.ModelSerializer):
    notify = serializers.SerializerMethodField()

    def get_notify(self, obj):
        return f"{obj.notify_in} {obj.notify_interval}"

    class Meta:
        model = CustomUrl
        read_only_fields = ["last_updated", ]
        fields = ["id", "name", "url", "slug", "last_updated", "notify", "last_updated", "acknowledged"]
