from django import forms

from web.models import Persons, Points, Product, Color, TranType, ProductTotal


class TablesFilterForm(forms.Form):
    ordering = forms.ChoiceField(label='Сортировка', required=False, choices=[
        ["products", "По алфавиту"],
        ["date", "По дате"]
    ])


class GeneralForm(forms.Form):
    class Meta:
        model = ProductTotal
        fields = '__all__'


# class EntryFormSet(forms.Form):
#     org = forms.ForeignKey(Organisation)

# class ProductTotal(models.Model):
#     surnames = models.ForeignKey(Persons, on_delete=models.CASCADE)
#     points = models.ForeignKey(Points, on_delete=models.CASCADE)
#     products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr')
#     products_packaging = models.IntegerField(blank=False, default=0)
#     products_cost = models.IntegerField(blank=False, default=0)
#     products_specification = models.TextField()
#     colors = models.ForeignKey(Color, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     date = models.DateField()
#     spec = models.ManyToManyField(Materials)
#     trans_type = models.ForeignKey(TranType, on_delete=models.CASCADE)
