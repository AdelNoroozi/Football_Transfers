from django.db import models


class Country(models.Model):
    CONTINENTS = (('AS', 'Asia'),
                  ('EUR', 'europe'),
                  ('NA', 'north America'),
                  ('SA', 'south America'),
                  ('OC', 'oceania'),
                  ('AFR', 'Africa'))
    name = models.CharField(max_length=30)
    continent = models.CharField(choices=CONTINENTS, max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
