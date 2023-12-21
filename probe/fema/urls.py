from django.urls import path
# from .views import show
from fema import views

urlpatterns = [
    path('show/', views.show, name='show'),
    path('data/', views.data, name='data'),
    path('updated/', views.updated, name='updated'),
    path('update1/', views.update1, name='update1'),
    path('latest/', views.latest, name='latest'),
    # path('date_filter/', views.date_filter, name='date_filter'),
    path('chart/', views.chart, name=''),
  
    path('get_data_for_popup/<str:table_name>/', views.get_data_for_popup, name='get_data_for_popup'),
   
    # path('count_colour/', views.count_colour, name='count_colour'),
    path('fema_datefilter/', views.fema_datefilter, name='fema_datefilter'),
    path('startup_datefilter/', views.startup_datefilter, name='startup_datefilter'),
    # path('dropdown/', views.dropdown, name='dropdown'),
    # path('dropfilter/', views.dropfilter, name='dropfilter'),
    # path('newdropdown/', views.newdropdown, name='newdropdown'),
    path('newhome/', views.newhome, name='newhome'),
    path('newfema_datefilter/', views.newfema_datefilter, name='newfema_datefilter'),
    path('newstartup_datefilter/', views.newstartup_datefilter, name='newstartup_datefilter'),
]
