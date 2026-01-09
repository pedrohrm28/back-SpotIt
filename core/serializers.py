from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import Item


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "is_active",
            "is_staff",
            "groups",
            "user_permissions",
            "password",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": "This field is required."})
        return attrs

    def create(self, validated_data):
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create_user(password=password, **validated_data)
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename", "content_type"]


class ItemSerializer(serializers.ModelSerializer):
    reporter = serializers.PrimaryKeyRelatedField(read_only=True)
    reporter_name = serializers.CharField(source="reporter.name", read_only=True)
    reporter_email = serializers.EmailField(source="reporter.email", read_only=True)
    reporter_phone = serializers.CharField(source="reporter.phone", read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "status",
            "category",
            "location",
            "event_date",
            "image_url",
            "contact_info",
            "receiver_name",
            "receiver_contact",
            "reporter",
            "reporter_name",
            "reporter_email",
            "reporter_phone",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "reporter"]

    def validate(self, attrs):
        status = attrs.get("status")
        receiver_name = attrs.get("receiver_name")
        receiver_contact = attrs.get("receiver_contact")

        if self.instance is not None:
            if status is None:
                status = self.instance.status
            if receiver_name is None:
                receiver_name = self.instance.receiver_name
            if receiver_contact is None:
                receiver_contact = self.instance.receiver_contact

        if status == Item.Status.RETURNED:
            if not receiver_name or not receiver_contact:
                raise serializers.ValidationError(
                    {
                        "receiver_name": "This field is required when status is returned.",
                        "receiver_contact": "This field is required when status is returned.",
                    }
                )

        return attrs


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email,
                password=password,
            )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code="authorization"
            )

        if not user:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials.", code="authorization"
            )

        attrs["user"] = user
        return attrs
