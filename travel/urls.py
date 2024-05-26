from django.contrib import admin
from django.urls import path
from App import views
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("cultural-experiences/info/", views.cultural, name="cultural"),
    path("customized-travel-packages/info/",
         views.customized, name="customized"),
    path("group-tours/info/", views.group, name="group"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("contact/", views.contact, name="contact"),
    path("book/", views.book_now, name="book"),
    path("book-data/", views.book_data, name="book_data"),
    path("your-book/", views.your_book, name="your_book"),
    path("approve-flight/<str:book_id>",
         views.approve_flight, name="approve_flight"),
    path("refuse-flight/<str:book_id>",
         views.refuse_flight, name="refuse_flight"),
    path("account/", views.account, name="account"),
    path("account/delete-account/", views.delete_acc, name="delete_acc"),
    path("account/change-password/", views.change_password, name="change_password"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("edit-user/<str:user_id>", views.edit_user, name="edit_user"),
    path("delete-user/<str:user_id>/", views.delete_user, name="delete_user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "App.views.not_found_error"
