from rest_framework import serializers
from . models import DatabaseConnection,DataModel,DataSource,Explorer
from django.contrib.auth.models import User
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from crishApp.utils import Util

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=DatabaseConnection
        fields= ['id','name','creation_user','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
        # exclude= ('creationUser',)
        
class DataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataModel
        fields= ['id','name','creation_user','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
        
class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields= ['id','name','creation_user','creationTime','lastUpdatedUser','lastUpdateTime','parameter']

class ExplorerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explorer
        fields= ['id','name','creation_user','creationTime','lastUpdatedUser','lastUpdateTime','parameter']
  
  
#User Related Serialzers      
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self,attrs):
      email=attrs.get('email')
      if User.objects.filter(email=email).exists():
        raise serializers.ValidationError("A user with that email already exists.")
      return attrs
        
class UserLoginSerialzer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']
        
        
class SendPasswordResetEmailSeializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields = ["email"]
    
    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password reset token',token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')