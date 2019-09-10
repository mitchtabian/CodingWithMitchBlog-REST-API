from rest_framework.response import Response

from account.models import CodingWithMitchAccount

def check_cwm_account(account):
	cwm_account = CodingWithMitchAccount.objects.get(account=account)
	if not cwm_account.is_membership_valid():
		data = {}
		data['response'] = 'You must become a member on Codingwithmitch.com to access the API. Visit https://codingwithmitch.com/enroll/'
		return Response(data)
	return None