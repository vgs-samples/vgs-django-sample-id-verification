from django.db import models


class PiiData(models.Model):
    social_security_number = models.CharField(max_length=200)
    driver_license_number = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.pub_date.__str__() + "  | SSN: " + self.social_security_number \
               + "; Driver License Number: " + self.driver_license_number
