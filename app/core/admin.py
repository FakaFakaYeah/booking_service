from sqladmin import ModelView

from app.models import Users, Bookings, Hotels, Rooms


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


class HotelAdmin(ModelView, model=Hotels):

    column_list = '__all__'
    name = "Отель"
    name_plural = "Отели"
    can_delete = False


class RoomAdmin(ModelView, model=Rooms):

    column_list = '__all__'
    name = "Комната"
    name_plural = "Комнаты"
    can_delete = False
