from django.shortcuts import render, HttpResponse
from .models import city
import json

from django.http import JsonResponse,request
from django.core.serializers import serialize
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseBadRequest

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from .forms import DateRangeFilterForm
from django.http import HttpResponseNotAllowed
from django.db.models import Min, Max

# def updated(request):
#     data = city.objects.all()[:7]
#     serialized_data = serialize('json', data)
#     return JsonResponse({'data': serialized_data}, safe=False)

# Create your views here.

def show(request):
    my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    return render(request, 'fema/index.html', {'my_dict': my_dict})


def data(request):
    data = city.objects.all()[:7]
     # Filter data based on the date range

    # Format the dates before passing them to the template
    formatted_data = []
    for item in data:
        formatted_date = item.Scraped_at.strftime('%d-%m-%Y') if item.Scraped_at else ''
        formatted_data.append({
            'table_name': item.table_name,
            'CountryCode': item.CountryCode,
            'Reason': item.Reason,
            'Data_Scraped': item.Data_Scraped,
            'Scraped_at': formatted_date,
        })

    # Pass the filtered and formatted data to the template
    context = {'data': formatted_data}
    return render(request, 'fema/base.html', context)

def updated(request):
    data = city.objects.all()[:7]
    print(data)
    # Filter data based on the date range

    # Format the dates before passing them to the template
    formatted_data = []
    for item in data:
        formatted_date = item.Scraped_at.strftime('%d-%m-%Y') if item.Scraped_at else ''
        formatted_data.append({
            'table_name': item.table_name,
            'CountryCode': item.CountryCode,
            'Reason': item.Reason,
            'Data_Scraped': item.Data_Scraped,
            'Scraped_at': formatted_date,
        })

    # Pass the filtered and formatted data to the template
    context = {'data': formatted_data}
    return render(request, 'fema/baseupdate.html', context)
   

def update1(request):
    data = city.objects.all()[:7]
    return render(request, 'fema/update1.html', {'data': data})


# def updated(request):
#     data = city.objects.all()[:7]
#     serialized_data = serialize('json', data)
#     return render(request, 'fema/baseupdate.html', {'data': data, 'serialized_data': serialized_data})

def latest(request):
    data = city.objects.all()[:7]
    print(data)
    return render(request, 'fema/latest.html', {'data': data})



def chart(request):
    cities = city.objects.all()[:5]
    labels = [city.table_name for city in cities]
    population = [city.Data_Scraped for city in cities]

    data = {
        'labels': labels,
        'population': population,
    }

    return render(request, 'fema/chart.html', {'data': data})






def fema_datefilter(request):
    # Filter data based on the 'table_name' (assuming 'fema')
    table_name_filter = 'fema'
    city_data = city.objects.filter(table_name=table_name_filter)
    
    data_range = city.objects.filter(table_name=table_name_filter)\
                    .aggregate(min_date=Min('scraped_at'), max_date=Max('scraped_at'))

    min_date = data_range['min_date'].strftime('%Y-%m-%d')
    max_date = data_range['max_date'].strftime('%Y-%m-%d')   

    # Date range filter form
    date_range_form = DateRangeFilterForm(request.GET)
    
    # Apply date range filter if form is valid
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data.get('start_date')
        end_date = date_range_form.cleaned_data.get('end_date')
        
        
        
        if start_date and end_date:
        #     city_data = city_data.filter(scraped_at__range=[start_date, end_date])
            if city_data.filter(scraped_at__range=[start_date, end_date]).exists():
                city_data = city_data.filter(scraped_at__range=[start_date, end_date])
        
            else:
                error_message = 'No data available for the selected date range. please select available dates'
                return render(request, 'fema/datefilter.html', {'error_message': error_message, 'min_date':min_date, 'max_date':max_date})


    # Format the dates before passing them to the template
    formatted_data = []
    for item in city_data:
        formatted_date = item.scraped_at.strftime('%d-%m-%Y') if item.scraped_at else ''
        formatted_data.append({
            'table_name': item.table_name,
            'status': item.status,
            'reason': item.reason,
            'data_scraped': item.data_scraped,
            'scraped_at': formatted_date,
        })
        
   
    # Pass the filtered and formatted data to the template
    context = {'city_data': formatted_data, 'date_range_form': date_range_form, 'min_date':min_date, 'max_date':max_date}
    
    return render(request, 'fema/datefilter.html', context)


def get_data_for_popup(request, table_name):
    today_date = timezone.now().date()
    data = city.objects.filter(table_name=table_name, scraped_at=today_date).first()

    if data:
        response_data = {
            'table_name': data.table_name,
            'status': data.status,
            'data_scraped': data.data_scraped,
            'reason': data.reason,
            'scraped_at': data.scraped_at.strftime('%Y-%m-%d'),
        }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(status=404)
    
    
    
# def count_colour(request):
#     end_date = timezone.now().date()
#     start_date = end_date - timedelta(days=7)

#     fema_data = city.objects.filter(table_name='fema', scraped_at__range=[start_date, end_date]).order_by('-scraped_at')
#     startup_data = city.objects.filter(table_name='startup india', scraped_at__range=[start_date, end_date]).order_by('-scraped_at')

#     data_list = []

#     for date in (end_date - timedelta(days=i) for i in range(7)):
#         fema_entry = fema_data.filter(scraped_at=date).first()
#         startup_entry = startup_data.filter(scraped_at=date).first()

#         fema_count = fema_entry.data_scraped if fema_entry else "-"
#         startup_count = startup_entry.data_scraped if startup_entry else "-"
#         fema_status = fema_entry.status if fema_entry else 'N/A'
#         startup_status = startup_entry.status if startup_entry else 'N/A'
#         fema_reason = fema_entry.reason if fema_entry else None
#         startup_reason = startup_entry.reason if startup_entry else None

#         # Determine the color based on status and reason
  
#         fema_color = (
#             'green' if fema_status == 'success' else
#             'orange' if fema_status == 'failure' and '204' in str(fema_reason) else
#             'red' if fema_status == 'failure' else
#             'black'
#         )

#         startup_color = (
#             'green' if startup_status == 'success' else
#             'orange' if startup_status == 'failure' and '204' in str(startup_reason) else
#             'red' if startup_status == 'failure' else
#             'black'
#         )   
             
#         data_list.append({
#             'Date': date.strftime('%Y-%m-%d'),
#             'FEMA_Count': fema_count,
#             'FEMA_Color': fema_color,
#             'Startup_India_Count': startup_count,
#             'Startup_India_Color': startup_color
#         })

#     context = {
#         'data_list': data_list,
#     }

#     return render(request, 'fema/count_colour.html', context)


def startup_datefilter(request):
    # Filter data based on the 'table_name' (assuming 'startup india')
    table_name_filter = 'startup india'
    city_data = city.objects.filter(table_name=table_name_filter)

    # Date range filter form
    date_range_form = DateRangeFilterForm(request.GET)

    # Apply date range filter if form is valid
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data.get('start_date')
        end_date = date_range_form.cleaned_data.get('end_date')
        if start_date and end_date:
            city_data = city_data.filter(scraped_at__range=[start_date, end_date])

    # Format the dates before passing them to the template
    formatted_data = []
    for item in city_data:
        formatted_date = item.scraped_at.strftime('%d-%m-%Y') if item.scraped_at else ''
        formatted_data.append({
            'table_name': item.table_name,
            'status': item.status,
            'reason': item.reason,
            'data_scraped': item.data_scraped,
            'scraped_at': formatted_date,
        })

    # Pass the filtered and formatted data to the template
    context = {'city_data': formatted_data, 'date_range_form': date_range_form}
    
    return render(request, 'fema/datefilter.html', context)



# def dropfilter(request):
#     if request.method == 'GET':
#         table_name_filter = 'fema'
#         city_data = city.objects.filter(table_name=table_name_filter)
        
#         data_range = city.objects.filter(table_name=table_name_filter)\
#                     .aggregate(min_date=Min('scraped_at'), max_date=Max('scraped_at'))

#         min_date = data_range['min_date'].strftime('%Y-%m-%d')
#         max_date = data_range['max_date'].strftime('%Y-%m-%d')   

#         date_range_form = DateRangeFilterForm(request.GET)
  
#         if date_range_form.is_valid():
#             start_date = date_range_form.cleaned_data.get('start_date')
#             end_date = date_range_form.cleaned_data.get('end_date')
            
        
            
            
#             if start_date and end_date:
#                 # Check if data is available within the selected date range
#                 if city_data.filter(scraped_at__range=[start_date, end_date]).exists():
#                     city_data = city_data.filter(scraped_at__range=[start_date, end_date])
                    
#                 else:
#                    error_message = 'No data available for the selected date range.please select the available dates'
#                    return render(request, 'fema/dropfilter.html', {'error_message': error_message, 'min_date':min_date, 'max_date':max_date})
        
#         formatted_data = []
#         for item in city_data:
#             formatted_date = item.scraped_at.strftime('%d-%m-%Y') if item.scraped_at else ''
#             formatted_data.append({
#                 'table_name': item.table_name,
#                 'status': item.status,
#                 'reason': item.reason,
#                 'data_scraped': item.data_scraped,
#                 'scraped_at': formatted_date,
#             })
         
#         context = {'city_data': formatted_data, 'date_range_form': date_range_form, 'min_date':min_date, 'max_date':max_date, 'error_message': error_message}
#         return render(request, 'fema/dropfilter.html', context)
    


def newhome(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)

    fema_data = city.objects.filter(table_name='fema', scraped_at__range=[start_date, end_date]).order_by('-scraped_at')
    startup_data = city.objects.filter(table_name='startup india', scraped_at__range=[start_date, end_date]).order_by('-scraped_at')

    data_list = []

    for date in (end_date - timedelta(days=i) for i in range(7)):
        fema_entry = fema_data.filter(scraped_at=date).first()
        startup_entry = startup_data.filter(scraped_at=date).first()

        fema_count = fema_entry.data_scraped if fema_entry else "-"
        startup_count = startup_entry.data_scraped if startup_entry else "-"
        fema_status = fema_entry.status if fema_entry else 'N/A'
        startup_status = startup_entry.status if startup_entry else 'N/A'
        fema_reason = fema_entry.reason if fema_entry else None
        startup_reason = startup_entry.reason if startup_entry else None

        # Determine the color based on status and reason
  
        fema_color = (
            'green' if fema_status == 'success' else
            'orange' if fema_status == 'failure' and '204' in str(fema_reason) else
            'red' if fema_status == 'failure' else
            'black'
        )
  
        startup_color = (
            'green' if startup_status == 'success' else
            'orange' if startup_status == 'failure' and '204' in str(startup_reason) else
            'red' if startup_status == 'failure' else
            'black'
        )  
    
        data_list.append({
            'Date': date.strftime('%Y-%m-%d'),
            'FEMA_Count': fema_count,
            'FEMA_Color': fema_color,
            'Startup_India_Count': startup_count,
            'Startup_India_Color': startup_color,
        
        })

    context = {
        'data_list': data_list
    }

    return render(request, 'fema/newhome.html', context)


def newfema_datefilter(request):
    # Filter data based on the 'table_name' (assuming 'fema')
    table_name_filter = 'fema'
    city_data = city.objects.filter(table_name=table_name_filter)
    
    data_range = city.objects.filter(table_name=table_name_filter)\
                    .aggregate(min_date=Min('scraped_at'), max_date=Max('scraped_at'))

    min_date = data_range['min_date'].strftime('%Y-%m-%d')
    max_date = data_range['max_date'].strftime('%Y-%m-%d')   

    # Date range filter form
    date_range_form = DateRangeFilterForm(request.GET)
    
    # Apply date range filter if form is valid
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data.get('start_date')
        end_date = date_range_form.cleaned_data.get('end_date')
        
        
        
        if start_date and end_date:
        #     city_data = city_data.filter(scraped_at__range=[start_date, end_date])
            if city_data.filter(scraped_at__range=[start_date, end_date]).exists():
                city_data = city_data.filter(scraped_at__range=[start_date, end_date])
        
            else:
                error_message = 'No data available for the selected date range. please select available dates'
                return render(request, 'fema/newdatefilter.html', {'error_message': error_message, 'min_date':min_date, 'max_date':max_date})


    # Format the dates before passing them to the template
    formatted_data = []
    for item in city_data:
        formatted_date = item.scraped_at.strftime('%d-%m-%Y') if item.scraped_at else ''
        
        # Updated data formatting to include color information Check status and set color accordingly
        status_color = (
            'green' if item.status== 'success' else
            'orange' if item.status == 'failure' and '204' in str(item.reason) else
            'red' 
        )
      
        formatted_data.append({
            'table_name': item.table_name,
            'status': item.status,
            'reason': item.reason,
            'data_scraped': item.data_scraped,
            'scraped_at': formatted_date,
            'status_color':status_color,
        })
        
   
    # Pass the filtered and formatted data to the template
    context = {'city_data': formatted_data, 'date_range_form': date_range_form, 'min_date':min_date, 'max_date':max_date,'table_name_filter':table_name_filter}
    
    return render(request, 'fema/newdatefilter.html', context)



def newstartup_datefilter(request):
    # Filter data based on the 'table_name' (assuming 'fema')
    table_name_filter = 'startup india'
    city_data = city.objects.filter(table_name=table_name_filter)
    
    data_range = city.objects.filter(table_name=table_name_filter)\
                    .aggregate(min_date=Min('scraped_at'), max_date=Max('scraped_at'))

    min_date = data_range['min_date'].strftime('%Y-%m-%d')
    max_date = data_range['max_date'].strftime('%Y-%m-%d')   

    # Date range filter form
    date_range_form = DateRangeFilterForm(request.GET)
    
    # Apply date range filter if form is valid
    if date_range_form.is_valid():
        start_date = date_range_form.cleaned_data.get('start_date')
        end_date = date_range_form.cleaned_data.get('end_date')
        
        
        
        if start_date and end_date:
        #     city_data = city_data.filter(scraped_at__range=[start_date, end_date])
            if city_data.filter(scraped_at__range=[start_date, end_date]).exists():
                city_data = city_data.filter(scraped_at__range=[start_date, end_date])
        
            else:
                error_message = 'No data available for the selected date range. please select available dates'
                return render(request, 'fema/newdatefilter.html', {'error_message': error_message, 'min_date':min_date, 'max_date':max_date})


    # Format the dates before passing them to the template
    formatted_data = []
    for item in city_data:
        formatted_date = item.scraped_at.strftime('%d-%m-%Y') if item.scraped_at else ''
        
        # Updated data formatting to include color information Check status and set color accordingly
        status_color = (
            'green' if item.status== 'success' else
            'orange' if item.status == 'failure' and '204' in str(item.reason) else
            'red' 
        )
      
        formatted_data.append({
            'table_name': item.table_name,
            'status': item.status,
            'reason': item.reason,
            'data_scraped': item.data_scraped,
            'scraped_at': formatted_date,
            'status_color': status_color,
        })
        
   
    # Pass the filtered and formatted data to the template
    context = {'city_data': formatted_data, 'date_range_form': date_range_form, 'min_date':min_date, 'max_date':max_date,'table_name_filter':table_name_filter}
    
    return render(request, 'fema/newdatefilter.html', context)



