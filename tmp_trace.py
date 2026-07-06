import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_portal.settings')
django.setup()

from accounts.models import User
from departments.models import Department
from api.views.employees import EmployeeV1ViewSet
from api.serializers import EmployeeSerializer

User.objects.filter(email='admin4@example.com').delete()

dept = Department.objects.create(name='Engineering', description='Engineering')
user = User.objects.create_user(email='admin4@example.com', password='12345', role='ADMIN', employee_id='EMP00004')
data = {
    'employee_id': 'EMP00005',
    'first_name': 'Ajay',
    'last_name': 'Kumar',
    'email': 'ajay4@example.com',
    'phone': '9876543210',
    'salary': '50000',
    'joining_date': '2024-01-01',
    'designation': 'Developer',
    'department_id': dept.id,
}
serializer = EmployeeSerializer(data=data)
print('valid', serializer.is_valid(), serializer.errors)
view = EmployeeV1ViewSet()
view.request = type('Req', (), {'user': user, 'data': data})()
try:
    result = view.perform_service_create(serializer.validated_data)
    print('saved', result)
except Exception:
    traceback.print_exc()
