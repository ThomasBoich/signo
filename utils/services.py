from django.core.paginator import Paginator

def paginate_list(request, list, page_len):
    paginator = Paginator(list, page_len)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)