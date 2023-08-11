from django.urls import path
from .views import EmployeeListView, EmployeeCreateView, EmployeeEditView, EmployeeDeleteView

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/edit/<int:employee_id>/', EmployeeEditView.as_view(), name='employee-edit'),
    path('employees/delete/<int:employee_id>/', EmployeeDeleteView.as_view(), name='employee-delete'),
]

