from api.repositories.department_repository import DepartmentRepository


class DepartmentService:
    repository = DepartmentRepository

    @classmethod
    def list_departments(cls):
        return cls.repository.list()

    @classmethod
    def get_department(cls, pk):
        return cls.repository.get(pk)

    @classmethod
    def create_department(cls, validated_data):
        return cls.repository.create(validated_data)

    @classmethod
    def update_department(cls, department, validated_data):
        return cls.repository.update(department, validated_data)

    @classmethod
    def delete_department(cls, department):
        return cls.repository.delete(department)
