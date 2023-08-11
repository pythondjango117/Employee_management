from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from .models import Employee
from .forms import EmployeeForm
from django.contrib import messages
from django.shortcuts import get_object_or_404

def dictfetchall(cursor):

    """
    Return all rows from a cursor as a list of dictionaries.

    Args:
        cursor (django.db.backends.utils.Cursor): The cursor object.

    Returns:
        list: A list of dictionaries representing the rows returned by the cursor.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


class EmployeeListView(View):
    """
    View to display a list of employees.

    Attributes:
        template_name (str): The name of the template used for rendering the view.
    """

    template_name = 'ems_app/employee_list.html'

    def get(self, request):
        """
        Handle GET requests for displaying a list of employees.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered template with a list of employees.
        """
        try:
            search_query = request.GET.get('q', '')  # Get the search query from the URL parameters

            with connection.cursor() as cursor:
                if search_query:
                    # Use a raw SQL query to search for employees based on the search query
                    query = "SELECT * FROM ems_app_employee WHERE first_name LIKE %s OR last_name LIKE %s"
                    cursor.execute(query, ['%' + search_query + '%', '%' + search_query + '%'])
                else:
                    cursor.execute("SELECT * FROM ems_app_employee")

                employees = dictfetchall(cursor)

            return render(request, self.template_name, {'employees': employees, 'search_query': search_query})

        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)})


class EmployeeCreateView(View):
    """
    View to create a new employee.

    Attributes:
        template_name (str): The name of the template used for rendering the view.
    """
    template_name = 'ems_app/employee_form.html'

    def get(self, request):
        """
        Handle GET requests for displaying the employee creation form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered template with the employee creation form.
        """
        try:
            form = EmployeeForm()
            return render(request, self.template_name, {'form': form})
        
        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)})

    def post(self, request):
        """
        Handle POST requests for creating a new employee.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirect to the employee list or an error template.
        """
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            department = request.POST.get('department')
            salary = request.POST.get('salary')
            task = request.POST.get('task')
            workinprog = request.POST.get('workinprog')
            role = request.POST.get('role')
            manager = request.POST.get('manager')
            phone = request.POST.get('phone')
            hire_date = request.POST.get('hire_date')

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ems_app_employee (first_name, last_name, email, department, salary, task, workinprog, role, manager, phone, hire_date) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            [first_name, last_name, email, department, salary, task, workinprog, role, manager, phone, hire_date])

            return redirect('employee-list')

        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)})    

class EmployeeEditView(View):
    """
    View to edit an employee.

    Attributes:
        template_name (str): The name of the template used for rendering the view.
    """
    template_name = 'ems_app/employee_form.html'

    def get(self, request, employee_id):
        """
        Handle GET requests for displaying the employee edit form.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee to be edited.

        Returns:
            HttpResponse: The rendered template with the employee edit form.
        """
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            form = EmployeeForm(instance=employee)
            return render(request, self.template_name, {'form': form, 'employee_id': employee_id})
        
        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)}) 

    def post(self, request, employee_id):
        """
        Handle POST requests for editing an employee.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee to be edited.

        Returns:
            HttpResponse: Redirect to the employee list or an error template.
        """
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            form = EmployeeForm(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('employee-list')
            return render(request, self.template_name, {'form': form, 'employee_id': employee_id})
        
        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)}) 
    

class EmployeeDeleteView(View):
    """
    View to delete an employee.

    Attributes:
        template_name (str): The name of the template used for rendering the view.
    """
    template_name = 'ems_app/employee_confirm_delete.html'

    def get(self, request, employee_id):
        """
        Handle GET requests for displaying the employee delete confirmation.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee to be deleted.

        Returns:
            HttpResponse: The rendered template for employee delete confirmation.
        """
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            return render(request, self.template_name, {'employee': employee})
        
        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)})

    def post(self, request, employee_id):
        """
        Handle POST requests for deleting an employee.

        Args:
            request (HttpRequest): The HTTP request object.
            employee_id (int): The ID of the employee to be deleted.

        Returns:
            HttpResponse: Redirect to the employee list or an error template.
        """
        try:
            employee = get_object_or_404(Employee, pk=employee_id)
            employee.delete()
            messages.success(request, 'Employee deleted successfully.')
            return redirect('employee-list')

        except Exception as e:
            messages.error(request, 'An error occurred while loading the form.')
            return render(request,  {'error_message': str(e)})