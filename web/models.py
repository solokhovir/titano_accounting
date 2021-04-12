from django.db import models
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.conf import settings


class Publication(models.Model):
    name = models.CharField(max_length=10000)
    date = models.DateTimeField()
    text = models.TextField()


# Создание базы данных с рабочими
class Persons(models.Model):
    surname = models.CharField('Фамилия', max_length=100)

    class Meta:
        verbose_name_plural = 'Фамилии'
        verbose_name = 'Фамилия'
        ordering = ['surname']

    def __str__(self):
        return self.surname


# Создание базы данных с участками
class Points(models.Model):
    point_name = models.CharField('Участок', max_length=500)

    class Meta:
        verbose_name_plural = 'Участки'
        verbose_name = 'Участок'
        ordering = ['point_name']

    def __str__(self):
        return self.point_name


# Создание базы данных с материалами
class Materials(models.Model):
    material_name = models.CharField('Наименование', max_length=500)

    def __str__(self):
        return self.material_name

    # М.б. подсчет через программу
    #     material_balance = models.IntegerField()
    #     material_minOrder = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Материалы'
        verbose_name = 'Материал'
        ordering = ['material_name']

    def __unicode__(self):
        return self.material_name


# Создание базы данных с деталями
class Detail(models.Model):
    detail_name = models.CharField('Наименование', max_length=500)
    detail_labor = models.IntegerField('Трудоемкость изготовления')
    detail_cost = models.IntegerField('Расценки')

    # detail_specification = models.CharField(max_length=1000)  добавить позже!!!

    class Meta:
        verbose_name_plural = 'Детали'
        verbose_name = 'Деталь'
        ordering = ['detail_name']

    def __str__(self):
        return self.detail_name

    def __int__(self):
        return self.detail_labor, self.detail_cost


# Создание базы данных с цветами
class Color(models.Model):
    color_name = models.CharField('Цвет', max_length=100)

    class Meta:
        verbose_name_plural = 'Цвета'
        verbose_name = 'Цвет'
        ordering = ['color_name']

    def __str__(self):
        return self.color_name


# Создание базы данных с изделиями
class Product(models.Model):
    product_name = models.CharField('Наименование', max_length=500)
    product_specification = models.ManyToManyField(Detail)
    product_packaging = models.IntegerField('Трудоемкость сборки, в сек')
    product_cost = models.IntegerField('Стоимость сборки, в руб')
    list_display = ("product_name", "product_packaging")

    class Meta:
        verbose_name_plural = 'Изделия'
        verbose_name = 'Изделие'
        ordering = ['product_name']

    def __str__(self):
        return self.product_name

    def __int__(self):
        return self.product_packaging, self.product_cost


# Создание базы данных с единицами измерения
class Unit(models.Model):
    unit_name = models.CharField('Единица измерения', max_length=100)

    class Meta:
        verbose_name_plural = 'Единицы измерения'
        verbose_name = 'Единица измерения'

    def __str__(self):
        return self.unit_name


# Создание базы данных с поставщиками
class Supplier(models.Model):
    supplier_name = models.TextField(max_length=5000)

    class Meta:
        verbose_name_plural = 'Поставщики'
        verbose_name = 'Поставщик'
        ordering = ['supplier_name']

    def __str__(self):
        return self.supplier_name


class TranType(models.Model):
    trtype = models.CharField('Тип', max_length=50)

    class Meta:
        verbose_name_plural = 'Типы'
        verbose_name = 'Тип'

    def __str__(self):
        return self.trtype


class ProductTotal(models.Model):
    surnames = models.ForeignKey(Persons, on_delete=models.CASCADE)
    points = models.ForeignKey(Points, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr')
    products_packaging = models.IntegerField(blank=False, default=0)
    products_cost = models.IntegerField(blank=False, default=0)
    products_specification = models.TextField()
    colors = models.ForeignKey(Color, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    spec = models.ManyToManyField(Materials)
    trans_type = models.ForeignKey(TranType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']


class DetailTotal(models.Model):
    surnames = models.ForeignKey(Persons, on_delete=models.CASCADE)
    points = models.ForeignKey(Points, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, related_name='det')
    colors = models.ForeignKey(Color, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details_labor = models.IntegerField(blank=False, default=0)
    details_cost = models.IntegerField(blank=False, default=0)
    date = models.DateField()
    trans_type = models.ForeignKey(TranType, on_delete=models.CASCADE)

    # details_specification = models.ForeignKey(Materials, on_delete=models.CASCADE, related_name='det_spec')

    class Meta:
        ordering = ['-date']


class MaterialTotal(models.Model):
    materials_name = models.ForeignKey(Materials, on_delete=models.CASCADE)
    colors = models.ForeignKey(Color, on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
    comment = models.TextField()
    units = models.ForeignKey(Unit, on_delete=models.CASCADE)
    trans_type = models.ForeignKey(TranType, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']


class GeneralProduct(models.Model):
    amount_prod = models.IntegerField()
    colors_prod = models.ForeignKey(Color, on_delete=models.CASCADE)
    points_prod = models.ForeignKey(Points, on_delete=models.CASCADE)
    product_gen = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prod_gen')
    # total = models.ForeignKey(Detail, on_delete=models.CASCADE, related_name='det_tot')


class GeneralDetail(models.Model):
    amount_det = models.IntegerField()
    colors_det = models.ForeignKey(Color, on_delete=models.CASCADE)
    points_det = models.ForeignKey(Points, on_delete=models.CASCADE)
    detail_gen = models.ForeignKey(Detail, on_delete=models.CASCADE, related_name='det_gen')


class GeneralMaterial(models.Model):
    amount_mat = models.IntegerField()
    colors_mat = models.ForeignKey(Color, on_delete=models.CASCADE)
    material_gen = models.ForeignKey(Materials, on_delete=models.CASCADE)
