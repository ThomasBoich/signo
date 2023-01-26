from documents.services import *
from django.db.models import Q, Count, When, Case
from django.db import models


def search_users(request, all_users):
    search_name = request.GET.get('search')
    period = request.GET.get('period')
    user_type = request.GET.get('user_type')
    
    # search_name may also be phone or email
    if search_name and len(search_name.split(' ')) == 1:
        all_users = all_users.filter((
            Q(first_name__icontains=search_name) | 
            Q(last_name__icontains=search_name)) |
            Q(phone__icontains=search_name) |
            Q(email__icontains=search_name)
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
        all_users = all_users.filter(date_joined__range=[start_date, end_date])

    if user_type:
        all_users = all_users.filter(type=user_type)

        
    sort_filter = request.GET.get('sort')
    if sort_filter:
        all_users = all_users.order_by(sort_filter)


    return all_users


def annotate_users_with_number_of_signed_docs(all_users, user_type):
    dict_true = {user_type:True}
    dict_false = {user_type:False}
    all_users = all_users.annotate(
                signed_docs=Count(Case(
                    When(**dict_true, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            ))) \
            .annotate(
                not_signed_docs=Count(Case(
                    When(**dict_false, then=1),
                    output_field=models.IntegerField(),
                    distinct=True
            )))

    return all_users