from sqladmin import ModelView

from app.models import Users, Bookings, Hotels, Rooms


class UserAdmin(ModelView, model=Users):

    column_list = [Users.id, Users.email, Users.bookings]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"


class BookingAdmin(ModelView, model=Bookings):

    column_list = '__all__'
    name = "Бронь"
    name_plural = "Брони"


class HotelAdmin(ModelView, model=Hotels):

    column_list = [
        Hotels.id, Hotels.name, Hotels.location, Hotels.services,
        Hotels.rooms, Hotels.rooms_quantity, Hotels.image_id
    ]
    column_details_list = column_list
    name = "Отель"
    name_plural = "Отели"
    can_delete = False


class RoomAdmin(ModelView, model=Rooms):

    column_list = [
        Rooms.id, Rooms.name, Rooms.description, Rooms.hotel, Rooms.price,
        Rooms.services, Rooms.bookings, Rooms.quantity, Rooms.image_id
    ]
    column_details_list = column_list
    name = "Комната"
    name_plural = "Комнаты"
    can_delete = False
