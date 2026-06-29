from accounts.models import User


class UserRepository:
    @staticmethod
    def list():
        return User.objects.all()

    @staticmethod
    def get(pk):
        return User.objects.get(pk=pk)
