from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionView.as_view()), 
    path('blocks/', views.BlockView.as_view()), 
    path('temps/<int:id>', views.TempView.as_view()), 
]