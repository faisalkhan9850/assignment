from rest_framework import serializers
from rest_framework.utils import json

from accounts.models import *
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'lastname', 'email', 'address', 'company', 'dob', 'device_type', 'device_token',
                  'auth_token', 'role')

    def get_auth_token(self, instance):
        try:
            return Token.objects.get(user=instance).key
        except:
            return ""

    def create(self, validated_data):
        request = self.context.get('request')
        first_name = request.data.get("first_name")
        lastname = request.data.get("lastname")
        address = request.data.get("address")
        company = request.data.get("company")
        email = request.data.get("email")
        dob = request.data.get("dob")
        user_role = request.data.get("user_role")
        device_type = request.data.get("device_type")
        device_token = request.data.get("device_token")
        password = request.data.get("password")
        social_id = request.data.get("social_id")
        user_obj = User.objects.create(first_name=first_name, lastname=lastname, address=address, company=company,
                                       dob=dob, email=email, device_type=device_type,
                                       device_token=device_token, social_id=social_id, role=user_role)
        if password:
            user_obj.set_password(password)
        user_obj.save()
        Token.objects.create(user=user_obj)
        return user_obj
