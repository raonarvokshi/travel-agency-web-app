from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMultiAlternatives  # Required to send emails
from django.template import loader  # Render templates on email body
from .models import Registered_emails, Book
from django.contrib import messages
from django.db.models import Q


def redirect_if_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already loged in")
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def redirect_if_not_authenticated(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in first")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def redirect_for_change_pass(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You need to login first")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def redirect_if_not_superuser(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return not_found_error(request, args)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.


def home(request):
    return render(request, "index.html")


@redirect_if_authenticated
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        verify_user = auth.authenticate(username=username, password=password)
        if not verify_user:
            messages.error(request, "Incorrect credentials")
            return redirect("login")

        auth.login(request, verify_user)
        messages.success(request, "You logged in successfully!")
        return redirect("home")

    return render(request, "login.html")


@redirect_if_authenticated
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            messages.error(request, "Username and email already exists!")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("register")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("register")

        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password)
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            messages.success(
                request, "Your account was created successfully! please confirm it by logging in")
            return redirect("login")

    else:
        return render(request, "register.html")


def logout(request):
    auth.logout(request)
    messages.success(request, "You logged out successfully")
    return redirect("home")


@redirect_if_not_authenticated
def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        full_name = f"{first_name} {last_name}"
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        user_message = request.POST.get("message")

        contact = Registered_emails()
        contact.first_name = first_name
        contact.last_name = last_name
        contact.full_name = full_name
        contact.email = email
        contact.subject = subject
        contact.message = user_message
        contact.user = request.user
        contact.save()
        messages.success(request, "Email sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")


def cultural(request):
    return render(request, "cultural.html")


def customized(request):
    return render(request, "customized.html")


def group(request):
    return render(request, "group.html")


@redirect_if_not_authenticated
def book_now(request):
    if request.method == "POST":
        destination = request.POST.get("destination")
        departure_date = request.POST.get("departure_date")
        return_date = request.POST.get("return_date")
        travelers = int(request.POST.get("travelers"))

        if travelers < 0:
            messages.error(
                request, "The number of travelers must be a positive number!")
            return redirect("book")
        elif travelers == 0:
            messages.error(
                request, "The number of travelers must be above 0!")
            return redirect("book")

        new_book = Book()
        new_book.destination = destination
        new_book.departure_date = departure_date
        new_book.return_date = return_date
        new_book.travelers = travelers
        new_book.user = request.user
        new_book.save()
        messages.success(request, "Your book request was sent successfully!")
        return redirect("book")

    return render(request, "book.html")


@redirect_if_not_authenticated
@redirect_if_not_superuser
def book_data(request):
    books = Book.objects.all()
    return render(request, "book_data.html", {"books": books})


@redirect_if_not_authenticated
def your_book(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "your_book.html", {"books": books})


@redirect_if_not_authenticated
@redirect_if_not_superuser
def approve_flight(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        approval_status = request.POST.get('approve')
        if approval_status == 'yes':
            book.not_approved = False
            book.approved = True
            book.pending = False
            book.save()
    return redirect('book_data')


@redirect_if_not_authenticated
@redirect_if_not_superuser
def refuse_flight(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        approval_status = request.POST.get('refuse')
        if approval_status == 'yes':
            book.approved = False
            book.not_approved = True
            book.pending = False
            book.save()

    return redirect('book_data')


@redirect_if_not_authenticated
def account(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":

        if (
            user.first_name != first_name or
            user.last_name != last_name or
            user.username != username or
            user.email != email
        ):
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Your account was updated successfully!")
            return redirect("account")
        else:
            messages.info(request, "No changes were made to your account.")
            return redirect("account")

    return render(request, "account.html")


@redirect_for_change_pass
def change_password(request):
    user_id = request.user.id
    current_user = request.user
    user_current_pass = request.POST.get("account_password")
    user_new_pass = request.POST.get("new_password")
    user_conf_new_pass = request.POST.get("confirm_new_password")

    if request.method == "POST":
        if current_user.check_password(user_current_pass):
            if user_new_pass == user_conf_new_pass:
                user = User.objects.get(id=user_id)
                user.set_password(user_conf_new_pass)
                user.save()
                messages.success(
                    request, "Please login with your new password!")
                return redirect("change_password")
            else:
                messages.error(
                    request, "Please enter the same password in both fields!")
                return redirect("change_password")
        else:
            messages.error(request, "Incorrect password!")
            return redirect("change_password")

    return render(request, "change_pass.html")


@redirect_if_not_authenticated
def delete_acc(request):
    user = request.user
    user_current_pass = request.POST.get("account_password")
    user_confirm_pass = request.POST.get("confirm_password")
    if request.method == "POST":
        if user_current_pass == user_confirm_pass:
            if user.check_password(user_current_pass):
                delete_user = User.objects.get(id=request.user.id)
                delete_user.delete()
                auth.logout(request)
                messages.success(
                    request, "Your account was deleted successfully!")
                return redirect("home")
            else:
                messages.error(request, "Incorrect Password!!")
                return redirect("delete_acc")
        else:
            messages.error(
                request, "Please enter the same password in both fields")
            return redirect("delete_acc")

    return render(request, "delete_acc.html")


@redirect_if_not_authenticated
@redirect_if_not_superuser
def manage_users(request):
    users = User.objects.all()
    return render(request, "manage_users.html", {"users": users})


@redirect_if_not_authenticated
@redirect_if_not_superuser
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")

    if request.method == "POST":
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "User Updated Successfully!")
            return redirect("manage_users")

    return render(request, "edit_user.html", {"user": user})


@redirect_if_not_authenticated
@redirect_if_not_superuser
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User Deleted Successfully!")
    return redirect("manage_users")


def not_found_error(request, exception):
    return render(request, "error_page.html", status=404)
