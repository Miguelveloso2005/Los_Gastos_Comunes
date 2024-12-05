from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('pending_expenses/', views.pending_expenses_view, name='pending_expenses'),
    path('mark_paid/<int:gasto_id>/', views.mark_paid, name='mark_paid'),
    path('generate_expenses/', views.generate_expenses_view, name='generate_expenses'),
    path('residente/', views.residente_view, name='residente'),
    path('pendientes/', views.pendientes, name='pendientes'),
    path('gasto/pagado/<int:gasto_id>/', views.marcar_como_pagado, name='marcar_como_pagado'),
    path('residente_pago/', views.residente_pago, name='residente_pago'),
    path('gasto/pagado/', views.marcar_gastos_pagados, name='marcar_gastos_pagados'),
    path('residente_form/', views.residente_form, name='residente_form'),




    
    


    

  
    path('', views.index_view, name='index'),  # Agrega esta línea para la raíz
]


