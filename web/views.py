from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.forms import model_to_dict, formset_factory, modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.db.models import F
from web import models as db
from tablib import Dataset
from .forms import GeneralForm
from web.resources import ProductTotalResource
from web.models import \
    Publication, \
    Persons, \
    Points, \
    Product, \
    Detail, \
    Materials, \
    Color, \
    Unit, \
    Supplier, \
    ProductTotal, \
    DetailTotal, \
    MaterialTotal, \
    TranType, \
    GeneralProduct, \
    GeneralDetail, \
    GeneralMaterial


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def login(request):
    return render(request, 'registration/login.html')


@login_required
def logged_out(request):
    return render(request, 'registration/logged_out.html')


# def publish(request):
#     if request.method == 'GET':
#         return render(request, 'publish.html')
#     else:
#         secret = request.POST['secret']
#         name = request.POST['name']
#         text = request.POST['text']
#
#         if secret != settings.SECRET_KEY:
#             return render(request, 'publish.html', {
#                 'error': 'Wrong secret key'
#             })
#         if len(name) == 0:
#             return render(request, 'publish.html', {
#                 'error': 'Empty name'
#             })
#         if len(text) == 0:
#             return render(request, 'publish.html', {
#                 'error': 'Empty text'
#             })
#
#         Publication(
#             name=name,
#             date=datetime.now(),
#             text=text.replace('\n', '<br />')
#         ).save()
#
#         return redirect('/publications')


@login_required
def publications(request):
    return render(request, 'publications.html', {
        'publications': Publication.objects.all()
    })


# def publication(request, number):
#     pubs = Publication.objects.filter(id=number)
#
#     if len(pubs) == 1:
#         pub = model_to_dict(pubs[0])
#         return render(request, 'publication.html', pub)
#     else:
#         return redirect('/')


@login_required
def product(request):
    if request.method == 'GET':
        cloneArea = GeneralForm(prefix='cloneArea')
        cloneArea1 = GeneralForm(prefix='cloneArea1')
        cloneArea2 = GeneralForm(prefix='cloneArea2')
        cloneArea3 = GeneralForm(prefix='cloneArea3')
        cloneArea4 = GeneralForm(prefix='cloneArea4')
        return render(request, 'product.html', {
            'persName': Persons.objects.all(),
            'pointName': Points.objects.all(),
            'prodName': Product.objects.all(),
            'materialsName': Materials.objects.all(),
            'colorName': Color.objects.all(),
            'unitName': Unit.objects.all(),
            'transaction': TranType.objects.all(),
        })
    else:
        surname = Persons.objects.get(surname=(request.POST['surname']))
        point = Points.objects.get(point_name=(request.POST['point']))
        production = Product.objects.get(product_name=(request.POST['production']))
        prod_id = production.id
        color = Color.objects.get(color_name=(request.POST['color']))
        amount = int(request.POST['amount'])
        amount_prod_gen = int(amount)
        date = request.POST['date']
        pr_pack = Product.objects.filter(pk=prod_id).values_list('product_packaging', flat=True).first()
        pr_cost = Product.objects.filter(pk=prod_id).values_list('product_cost', flat=True).first()

        pr_spec = Product.objects.filter(pk=prod_id).values_list('product_specification', flat=True).all()
        # pr_spec = Product.objects.filter(product_specification=prod_id).all()
        # pr_spec = Product.objects.get(product_specification=(request.POST['product_specification']))

        trtype = TranType.objects.get(pk=(request.POST['trtype']))
        # form1 = GeneralForm(prefix='cloneArea')
        cloneArea = GeneralForm(request.POST, prefix=request.GET.get('cloneArea'))
        cloneArea1 = GeneralForm(request.POST, prefix=request.GET.get('cloneArea1'))
        cloneArea2 = GeneralForm(request.POST, prefix=request.GET.get('cloneArea2'))
        # cloneArea = GeneralForm(request.POST, prefix='cloneArea')
        # cloneArea1 = GeneralForm(request.POST, prefix='cloneArea1')
        # cloneArea2 = GeneralForm(request.POST, prefix='cloneArea2')
        # prefix = GeneralForm.request.GET.get('cloneArea')
        # clone_area = mdl.EntryFormSet(request.POST, prefix="cloneArea")
        # formset = product_clone(product, request.POST)
        # instances = [product_clone]
        # pr_spec = request.GET.getlist('prod_id')
        # for key in pr_spec:
        #     Product.objects.get(product_specification=pr_spec, prod_id=int(key))
        # clone_area = {
        #     'key': {
        #         'key': cloneArea,
        #     },
        #     'key2': {
        #         'key': cloneArea1,
        #     },
        # }
        # for key in clone_area.forms:
        if trtype.id == 1:
            if GeneralProduct.objects.filter(product_gen=production, points_prod=point, colors_prod=color).exists():
                general_old_delete_id = GeneralProduct.objects.get(product_gen=production, points_prod=point,
                                                                   colors_prod=color).id
                old_amount = int(GeneralProduct.objects.filter(pk=general_old_delete_id).values_list('amount_prod',
                                                                                                     flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralProduct.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_prod_gen = amount + old_amount
                GeneralProduct(
                    product_gen=production,
                    points_prod=point,
                    colors_prod=color,
                    amount_prod=amount_prod_gen,
                ).save()
                ProductTotal(
                    surnames=surname,
                    points=point,
                    products=production,
                    colors=color,
                    amount=amount,
                    date=date,
                    products_packaging=pr_pack,
                    products_cost=pr_cost,
                    products_specification=pr_spec,
                    trans_type=trtype
                ).save()
            else:
                GeneralProduct(
                    product_gen=production,
                    points_prod=point,
                    colors_prod=color,
                    amount_prod=amount_prod_gen,
                ).save()
                ProductTotal(
                    surnames=surname,
                    points=point,
                    products=production,
                    colors=color,
                    amount=amount,
                    date=date,
                    products_packaging=pr_pack,
                    products_cost=pr_cost,
                    products_specification=pr_spec,
                    trans_type=trtype
                ).save()
        elif trtype.id == 2:
            if GeneralProduct.objects.filter(product_gen=production, points_prod=point, colors_prod=color).exists():
                general_old_delete_id = GeneralProduct.objects.get(product_gen=production, points_prod=point,
                                                                   colors_prod=color).id
                old_amount = int(GeneralProduct.objects.filter(pk=general_old_delete_id).values_list('amount_prod',
                                                                                                     flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralProduct.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_prod_gen = old_amount - amount
                GeneralProduct(
                    product_gen=production,
                    points_prod=point,
                    colors_prod=color,
                    amount_prod=amount_prod_gen,
                ).save()

        context = {'cloneArea': cloneArea, 'cloneArea1': cloneArea1, 'cloneArea2': cloneArea2}
        return redirect('/product_total', context)


@login_required
def details(request):
    if request.method == 'GET':
        return render(request, 'details.html', {
            'persName': Persons.objects.all(),
            'pointName': Points.objects.all(),
            'detailName': Detail.objects.all(),
            'colorName': Color.objects.all(),
            'transaction': TranType.objects.all()
        })
    else:
        surname = Persons.objects.get(surname=(request.POST['surname']))
        point = Points.objects.get(point_name=(request.POST['point']))
        details_name = Detail.objects.get(detail_name=(request.POST['details']))
        det_id = details_name.id
        color = Color.objects.get(color_name=(request.POST['color']))
        amount = int(request.POST['amount'])
        amount_det_gen = int(amount)
        date = request.POST['date']
        det_lab = Detail.objects.filter(pk=det_id).values_list('detail_labor', flat=True).first()
        det_cost = Detail.objects.filter(pk=det_id).values_list('detail_cost', flat=True).first()
        trtype = TranType.objects.get(pk=(request.POST['trtype']))

        if trtype.id == 1:
            if GeneralDetail.objects.filter(detail_gen=details_name, points_det=point, colors_det=color).exists():
                general_old_delete_id = GeneralDetail.objects.get(detail_gen=details_name, points_det=point,
                                                                  colors_det=color).id
                old_amount = int(
                    GeneralDetail.objects.filter(pk=general_old_delete_id).values_list('amount_det', flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralDetail.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_det_gen = amount + old_amount
                GeneralDetail(
                    detail_gen=details_name,
                    points_det=point,
                    colors_det=color,
                    amount_det=amount_det_gen,
                ).save()
                DetailTotal(
                    surnames=surname,
                    points=point,
                    detail=details_name,
                    colors=color,
                    amount=amount,
                    date=date,
                    details_labor=det_lab,
                    details_cost=det_cost,
                    trans_type=trtype
                ).save()
            else:
                GeneralDetail(
                    detail_gen=details_name,
                    points_det=point,
                    colors_det=color,
                    amount_det=amount_det_gen,
                ).save()
                DetailTotal(
                    surnames=surname,
                    points=point,
                    detail=details_name,
                    colors=color,
                    amount=amount,
                    date=date,
                    details_labor=det_lab,
                    details_cost=det_cost,
                    trans_type=trtype
                ).save()
        elif trtype.id == 2:
            if GeneralDetail.objects.filter(detail_gen=details_name, points_det=point, colors_det=color).exists():
                general_old_delete_id = GeneralDetail.objects.get(detail_gen=details_name, points_det=point,
                                                                  colors_det=color).id
                old_amount = int(
                    GeneralDetail.objects.filter(pk=general_old_delete_id).values_list('amount_det', flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralDetail.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_det_gen = old_amount - amount
                GeneralDetail(
                    detail_gen=details_name,
                    points_det=point,
                    colors_det=color,
                    amount_det=amount_det_gen,
                ).save()

        return redirect('/detail_total')


@login_required
def materials(request):
    if request.method == 'GET':
        return render(request, 'materials.html', {
            'materialsName': Materials.objects.all(),
            'colorName': Color.objects.all(),
            'suppName': Supplier.objects.all(),
            'unName': Unit.objects.all(),
            'transaction': TranType.objects.all()
        })
    # elif request.method == 'POST':
    else:
        material_name = Materials.objects.get(material_name=(request.POST['material']))
        supplier = Supplier.objects.get(supplier_name=(request.POST['supplier']))
        color = Color.objects.get(color_name=(request.POST['color']))
        amount = int(request.POST['amount'])
        amount_mat_gen = int(amount)
        date = request.POST['date']
        comment = request.POST['comment']
        unit = Unit.objects.get(pk=(request.POST['unit']))
        trtype = TranType.objects.get(pk=(request.POST['trtype']))

        if trtype.id == 1:
            if GeneralMaterial.objects.filter(material_gen=material_name, colors_mat=color).exists():
                general_old_delete_id = GeneralMaterial.objects.get(material_gen=material_name, colors_mat=color).id
                old_amount = int(GeneralMaterial.objects.filter(pk=general_old_delete_id).values_list('amount_mat',
                                                                                                      flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralMaterial.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_mat_gen = amount + old_amount
                GeneralMaterial(
                    material_gen=material_name,
                    colors_mat=color,
                    amount_mat=amount_mat_gen,
                ).save()
                MaterialTotal(
                    materials_name=material_name,
                    suppliers=supplier,
                    colors=color,
                    amount=amount,
                    date=date,
                    comment=comment,
                    units=unit,
                    trans_type=trtype
                ).save()
            else:
                GeneralMaterial(
                    material_gen=material_name,
                    colors_mat=color,
                    amount_mat=amount_mat_gen,
                ).save()
                MaterialTotal(
                    materials_name=material_name,
                    suppliers=supplier,
                    colors=color,
                    amount=amount,
                    date=date,
                    comment=comment,
                    units=unit,
                    trans_type=trtype
                ).save()
        elif trtype.id == 2:
            if GeneralMaterial.objects.filter(material_gen=material_name, colors_mat=color).exists():
                general_old_delete_id = GeneralMaterial.objects.get(material_gen=material_name, colors_mat=color).id
                old_amount = int(GeneralMaterial.objects.filter(pk=general_old_delete_id).values_list('amount_mat',
                                                                                                      flat=True).first())
                # print(old_amount)
                general_old_delete = GeneralMaterial.objects.get(id=general_old_delete_id)
                general_old_delete.delete()
                amount_mat_gen = old_amount - amount
                GeneralMaterial(
                    material_gen=material_name,
                    colors_mat=color,
                    amount_mat=amount_mat_gen,
                ).save()

        return redirect('/materials_total')


@login_required
def product_total(request):
    return render(request, 'product_total.html', {
        'product_total': ProductTotal.objects.all(),
    })


@login_required
def detail_total(request):
    return render(request, 'detail_total.html', {
        'detail_total': DetailTotal.objects.all()
    })


@login_required
def material_total(request):
    return render(request, 'materials_total.html', {
        'materials_total': MaterialTotal.objects.all()
    })


@login_required
def general_table(request):
    return render(request, 'general_table.html', {
        'general_product': GeneralProduct.objects.all(),
        'general_detail': GeneralDetail.objects.all(),
        'general_material': GeneralMaterial.objects.all()
    })
    # general_product = Product.objects.all()
    # return render(request, 'general_table.html')


@login_required
def delete_product(request, id):
    product_delete = ProductTotal.objects.get(pk=id)
    product_delete.delete()
    return HttpResponseRedirect("/product_total")


@login_required
def delete_detail(request, id):
    detail_delete = DetailTotal.objects.get(pk=id)
    detail_delete.delete()
    return HttpResponseRedirect("/detail_total")


@login_required
def delete_material(request, id):
    material_delete = MaterialTotal.objects.get(pk=id)
    material_delete.delete()
    return HttpResponseRedirect("/materials_total")


@login_required
def delete_general_product(request, id):
    general_product = GeneralProduct.objects.get(pk=id)
    general_product.delete()
    return HttpResponseRedirect("/general_table")


@login_required
def delete_general_detail(request, id):
    general_detail = GeneralDetail.objects.get(pk=id)
    general_detail.delete()
    return HttpResponseRedirect("/general_table")


@login_required
def delete_general_material(request, id):
    general_material = GeneralMaterial.objects.get(pk=id)
    general_material.delete()
    return HttpResponseRedirect("/general_table")

# def listing(request):
#     contact_list = product.objects.all()
#     paginator = Paginator(contact_list, 4) # Show 25 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'pagination.html', {'page_obj': page_obj})
