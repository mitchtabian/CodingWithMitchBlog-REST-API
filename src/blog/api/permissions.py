from rest_framework.permissions import BasePermission

from account.models import Account, CodingWithMitchAccount
from limit.models import DAILY_REQUEST_LIMIT, DailyRequestLimit, DAILY_BLOG_POST_LIMIT, DailyBlogPostLimit
from limit.utils import increment_daily_requests

class IsCodingWithMitchMember(BasePermission):

	message = 'You must become a member on Codingwithmitch.com to access the API. Visit https://codingwithmitch.com/enroll/'

	def has_permission(self, request, view):
		cwm_account = CodingWithMitchAccount.objects.get(account=request.user)
		if not cwm_account.is_membership_valid():
			return False
		return True


class HasReachedDailyRequestLimit(BasePermission):

	message = "You've exceeded %s requests today. Wait until 12pm PST for it to reset." %DAILY_REQUEST_LIMIT

	def has_permission(self, request, view):
		daily_limits = increment_daily_requests(request.user)
		if daily_limits.is_daily_limit_exceeded():
			return False
		return True


class HasReachedDailyBlogPostLimit(BasePermission):

	message = "You've created %s blog posts today. Wait until 12pm PST for it to reset." %DAILY_BLOG_POST_LIMIT

	def has_permission(self, request, view):
		daily_limits, created = DailyBlogPostLimit.objects.get_or_create(
										account=request.user
									)
		if daily_limits.is_daily_limit_exceeded():
			return False
		return True



