from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    """
    Social Login serializer
    """

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True
    )
    access_token_secret = serializers.CharField(
        max_length=300, allow_null=True, default=None, trim_whitespace=True
    )
