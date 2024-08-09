from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields= ['id','email','nom','password']
        
    # def validate_email(self, value):
    #     """
    #     Check if the email already exists.
    #     """
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("le compt est deja exist verifier ton email")
    #     return value
        
    