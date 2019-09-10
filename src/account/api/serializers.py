from rest_framework import serializers

from account.models import Account
from account.utils import update_codingwithmitch_member_subcription


class RegistrationSerializer(serializers.ModelSerializer):

	password2 				= serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}

	def	save(self):
		email = self.validated_data.get('email')
		username = self.validated_data.get('username')
		account = Account(
					email=email,
					username=username
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()
		update_codingwithmitch_member_subcription(account)
		return account


class AccountPropertiesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['pk', 'email', 'username', ]



class ChangePasswordSerializer(serializers.Serializer):

	old_password 				= serializers.CharField(required=True)
	new_password 				= serializers.CharField(required=True)
	confirm_new_password 		= serializers.CharField(required=True)
