from fastapi import HTTPException, status


class CustomExceptions(HTTPException):

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserExistsException(CustomExceptions):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь с такими учетными данными уже зарегистрирован!'


class UserNotFoundException(CustomExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь с такими учетными данными не зарегистрирован!'


class InvalidAuthDataException(CustomExceptions):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Вы ввели неверные учетные данные'
