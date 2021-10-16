from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .settings import get_page_size

def get_paginator(request, object_list):

    paginator = Paginator(object_list, get_page_size())  # 3 post per page

    page_number = request.GET.get('page')

    try:
        paginator_object = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        paginator_object = paginator.page(1)
    except EmptyPage:
        page_number = paginator.num_pages
        paginator_object = paginator.page(paginator.num_pages)

    return page_number, paginator_object