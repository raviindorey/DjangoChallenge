from django.db import models
from django.contrib.auth.models import User

# A UserAddress is saved every time the user changes something in the form,
#  provided the form is valid.
# The task is devising a way of removing partial addresses that are entirely a
#  subset of the current address.
# For example, assuming the following addresses are entered in the form(all
#  belonging to the same user) in sequence:
#
# add1 = UserAddress(name="Max", city="Giventown")
# add2 = UserAddress(name="Max Mustermann", street_address="Randomstreet",
#  city="Giventown")
# add3 = UserAddress(name="Max Mustermann", street_address="456 Randomstreet",
#  city="Giventown")
# add4 = UserAddress(name="Max Mustermann", street_address="789 Otherstreet",
#  city="Giventown", country="NL")
#
# The expected result would be that only add3 and add4 are left in the DB at
#  the end of the sequence

# NOTE:
# According to the given model, a user can have multiple addresses
# I will try to save only those addresses that fits the criteria
# 'country' is made optional so add3 can be saved too
# 'created' is added later for sorting purposes


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    street_address_line2 = models.CharField(max_length=255, blank=True,
                                            null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=2, blank=True, null=True)
    full_address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_full_address(self):
        streetdata = f"{self.street_address}\n{self.street_address_line2}"
        return f"{streetdata}\n{self.zipcode} {self.city}\
            {self.state} {self.country}"

    def save(self, *args, **kwargs):
        self.full_address = self.get_full_address()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
