from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    # path('equipment/<int:id>/', views.equipment_detail, name='equipment_details'),
    path('equipment/type/<str:type_name>/', views.equipment_by_type, name='equipment_by_type'),
    path('equipment/<int:id>/', views.equipment_detail, name='equipment_detail'),
    path('signup/', views.signup, name='signup'),
    path('supplier-dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('my-equipment/', views.my_equipment, name='my_equipment'),
    path('login/', views.user_login, name='login'),
    path('add-equipment/', views.add_equipment, name='add_equipment'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-equipment/<int:id>/', views.edit_equipment, name='edit_equipment'),
    path('delete-equipment/<int:id>/', views.delete_equipment, name='delete_equipment'),
    path('rent/<int:id>/', views.rent_equipment, name='rent_equipment'),
    path('rental-requests/', views.rental_requests, name='rental_requests'),
    path('approve-request/<int:id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:id>/', views.reject_request, name='reject_request'),
    path('supplier/requests/', views.supplier_requests, name='supplier_requests'),
    path('supplier/profile/', views.supplier_profile, name='supplier_profile'),
    path('my-requests/',views.my_requests,name='my_requests'),
]
