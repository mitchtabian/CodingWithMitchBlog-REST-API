from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from account.api.serializers import RegistrationSerializer, AccountPropertiesSerializer
from account.models import Account
from rest_framework.authtoken.models import Token

# Register
# Response: https://gist.github.com/mitchtabian/c13c41fa0f51b304d7638b7bac7cb694
# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):

	if request.method == 'POST':
		data = {}
		email = request.data.get('email', '0')
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username


# Account properties
# Response: https://gist.github.com/mitchtabian/4adaaaabc767df73c5001a44b4828ca5
# Url: https://<your-domain>/api/account/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):

	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = AccountPropertiesSerializer(account)
		return Response(serializer.data)


# Account update properties
# Response: https://gist.github.com/mitchtabian/72bb4c4811199b1d303eb2d71ec932b2
# Url: https://<your-domain>/api/account/properties/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):

	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = AccountPropertiesSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = 'Account update success'
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# LOGIN
# Response: https://gist.github.com/mitchtabian/8e1bde81b3be342853ddfcc45ec0df8a
# URL: https://<your-domain>/api/account/login
class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)







