from django.urls import path
from .views import CartDetailView, CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart-list-create'),
    path('<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
]
