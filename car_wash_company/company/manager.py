from django.core.exceptions import ValidationError
from django.db.models import Manager


class WasherManager(Manager):
    def get_random_washer(self, branch):
        try:
            return self.filter(branch_id=branch, is_free=True).order_by('?')[0]
        except:
            raise ValidationError('ყველა მრეცხავი დაკავუბულია')