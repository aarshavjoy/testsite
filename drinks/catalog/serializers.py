from rest_framework import serializers
from .models import Drink
from django.contrib.auth.models import User
from django.contrib.auth import authenticate



class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        exclude=[]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Incorrect username or password")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        data['user'] = user
        return data






class Drinkserializer(serializers.ModelSerializer):
    class Meta:
        model=Drink
        feilds =['id','name','description']
        exclude = []



class DrinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drink
        fields = ['id', 'name', 'description']
        exclude=[]

    