from documents.services import *

def search_users(request, all_users):
    search_name = request.GET.get('search')
    period = request.GET.get('period')
    
    if search_name and len(search_name.split(' ')) == 1:
        all_users = all_users.filter(
            Q(first_name__icontains=search_name) | 
            Q(last_name__icontains=search_name)
            )
    elif search_name and len(search_name.split(' ')) == 2:
        name1 = search_name.split(' ')[0]
        name2 = search_name.split(' ')[1]
        all_users = all_users.filter(
            Q(first_name__icontains=name1) & Q(last_name__icontains=name2) |
            Q(first_name__icontains=name2) & Q(last_name__icontains=name1)
        )

    # get_dates is in documents.services
    if period:
        start_date, end_date = get_dates(period, all_users) 
        all_users = all_users.filter(last_login__range=[start_date, end_date])

    return all_users