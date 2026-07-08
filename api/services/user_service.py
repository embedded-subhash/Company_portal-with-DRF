from api.repositories.user_repository import UserRepository


class UserService:
    repository = UserRepository

    @classmethod
    def list_users(cls):
        return cls.repository.list()

    @classmethod
    def get_user(cls, pk):
        return cls.repository.get(pk)
