from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    
    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
      model = User
      fields = ['id', 'username', 'email' , 'password', 'first_name',
                'last_name', 'is_superuser', ]
      extra_kwargs = {
          "password" : {"write_only": True},
          "is_superuser" : {"read_only": True}
      }
