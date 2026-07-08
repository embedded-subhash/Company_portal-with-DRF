from departments.models import Department


class DepartmentRepository:
    @staticmethod
    def list():
        return Department.objects.prefetch_related("employees").all()

    @staticmethod
    def get(pk):
        return Department.objects.prefetch_related("employees").get(pk=pk)

    @staticmethod
    def create(validated_data):
        return Department.objects.create(**validated_data)

    @staticmethod
    def update(department, validated_data):
        for field, value in validated_data.items():
            setattr(department, field, value)
        department.save()
        return department

    @staticmethod
    def delete(department):
        department.delete()
