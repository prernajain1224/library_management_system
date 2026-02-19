from django.urls import path
from .views import issue_book,return_book,my_books,book_list,search_book,my_profile,student_issued_book,CreateUserView,LoginView,AddBookView

urlpatterns = [
    path('issue/<int:book_id>/<int:student_id>', issue_book),
    path('issue/<int:issue_id>', return_book),
    path('my-books', my_books),

    path('books', book_list),
    path('books/search', search_book),
    # path('profile', my_profile),
    path('profile', my_profile.as_view()),
    path('student/books', student_issued_book),


    path('create-user', CreateUserView.as_view()),
    path('login', LoginView.as_view()),
    path('books', AddBookView.as_view()),





]
