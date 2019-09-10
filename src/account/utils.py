import requests
from datetime import date
from datetime import datetime

from account.models import CodingWithMitchAccount

MEMBERSHIP_EXPIRED = 'MEMBERSHIP EXPIRED'
MEMBERSHIP_VALID = 'MEMBERSHIP VALID'
MEMBERSHIP_DNE = 'MEMBERSHIP DOES NOT EXIST'
MEMBERSHIP_TEMP_ACCESS = 'TEMPORARY FREE ACCESS'

# Check URL: https://codingwithmitch.com/account/check_member_status/?email=mitch@tabian.ca
def is_codingwithmitch_member(account):
	try:
		url = 'https://codingwithmitch.com/account/check_member_status/?email=%s' %(account.email)
		r = requests.get(url=url)
		data = r.json()
	except Exception:
		return None
	
	result = data['result']
	if result != MEMBERSHIP_VALID and result != MEMBERSHIP_TEMP_ACCESS:
		return None
	return data['valid_until']


def update_codingwithmitch_member_subcription(account):
	try:
		cwm_account = CodingWithMitchAccount.objects.get(account=account)
	except CodingWithMitchAccount.DoesNotExist:
		cwm_account = CodingWithMitchAccount(
						account=account,
						cwm_member_valid_until=None,
					)
	is_valid_until = is_codingwithmitch_member(account)
	if is_valid_until != None:
		is_valid_until = datetime.strptime(is_valid_until, '%Y-%m-%d').date()
	cwm_account.cwm_member_valid_until = is_valid_until
	cwm_account.save()
	return cwm_account

	





