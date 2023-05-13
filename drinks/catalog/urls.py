from django.urls import path,include
from .import views

urlpatterns = [
    path('drink',views.drink_list),
    path('drink/<int:id>',views.drink_details),
    path('signup/', views.signup, name='signup'),
    path('simpleapi',views.simpleapi),
    path('login/', views.login, name='login'),
    path('drinks/search/', views.search, name='search'),
]
