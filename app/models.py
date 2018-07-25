from django.db import models


class PiiData(models.Model):
    social_security_number = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.pub_date.__str__() + "  | SSN: " + self.social_security_number \
               + "; National id: " + self.national_id
