import datetime
from django.db import models

class Utenza(models.Model):
    CF = models.CharField(max_length=200)
    Nome=models.CharField(max_length=200)
    Cognome=models.CharField(max_length=200)
    DataNascita=models.DateField()

    def __str__(self):
        return self.CF

    def getAnnoFromCF(self):
        year = self.CF[6] + self.CF[7]
        currentYear = datetime.date.strftime(datetime.date.today(), "%Y")
        lastDigitCurrentYear = currentYear[2] + currentYear[3]
        if (int(year) <= int(lastDigitCurrentYear) and int(year) >= 0):
            return datetime.date.strftime(datetime.date(int("20"+year), 1, 1), "%Y")
        return datetime.date.strftime(datetime.date(int("19"+year), 1, 1), "%Y")