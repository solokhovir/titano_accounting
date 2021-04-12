from django.db import models
from import_export import resources
from .models import ProductTotal, Persons, Points, Product, Color


class ProductTotalResource(resources.ModelResource):

    class Meta:
        model = ProductTotal

        # def __str__(self):
        #     return self.
