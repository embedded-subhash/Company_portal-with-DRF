from django.core.mail import send_mail


def send_employee_email(employee):
    send_mail(
        subject="Welcome",
        message="Welcome Employee",
        from_email="hr@company.com",
        recipient_list=[employee.email]
    )
