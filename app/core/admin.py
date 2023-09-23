from sqladmin import ModelView

from app.models import Users, Bookings


class UserAdmin(ModelView, model=Users):

    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"


class BookingAdmin(ModelView, model=Bookings):

    column_list = '__all__'
    name = "Бронь"
    name_plural = "Брони"



