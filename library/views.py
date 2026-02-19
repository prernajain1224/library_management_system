from django.shortcuts import render
from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required
from .models import Book ,IssuedBook
from datetime import date
from django.http import JsonResponse
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import ProfileSerializer,BookSerializer,LoginSerializer,CreateUserSerializer
from django.contrib.auth.models import User


@login_required
def issue_book(request,book_id,student_id):
    if request.user.profile.role != "LIBRARIAN":
        return JsonResponse({"error": "Unauthorized"}, status = 403)
    
    book = Book.objects.get(id=book_id)

    if not book.is_available:
        return JsonResponse({"error": "Book not available"})
    
    IssuedBook.objects.create(
        book=book,
        student_id=student_id
    )

    book.is_available = False
    book.save()

    return JsonResponse({"message": "Book issued successfully"}, status = 200)


@login_required
def return_book(request,issue_id):
    if request.user.profile.role != "LIBRARIAN":
        return JsonResponse({"error": "Unauthorized"}, status = 403)
    
    issue  = IssuedBook.objects.get(id = issue_id)
    issue.return_date = date.today()
    issue.save()

    return JsonResponse({"message": "Book return successfully"}, status = 200)


@login_required
def my_books(request):
    issues = IssuedBook.objects.filter(student = request.user)

    data  = []

    for issue in issues:
        days = (date.today() - issue.issue_date).days
        fine = (days - 7) * 10 if days > 7 else 0

        data.append({
            "book_name" : issue.book.name,
            "issue_date" : issue.issue_date,
            "fine" : fine
        })

    return JsonResponse(data,safe=False)



@login_required
def book_list(request):
    if request.user.profile.role != "LIBRARIAN":
        return JsonResponse({"error": "Unauthorized"}, status = 403)
    
    books = Book.objects.all()
    data = []

    for book in books:
        data.append({
            "id" : book.id,
            "name" : book.name,
            "author" : book.author,
            "is_available" : book.is_available
        })

    return JsonResponse(data,safe=False)

@login_required
def search_book(request):
    if request.user.profile.role != "LIBRARIAN":
        return JsonResponse({"error": "Unauthorized"}, status = 403)
    
    name = request.Get.get("name")

    books = Book.objects.filter(name__icontains=name)
    data = [{"id" : b.id, "name":b.name} for b in books]

    return JsonResponse(data,safe=False)

# @login_required
# def my_profile(request):
#     profile = request.user.profile

#     return JsonResponse({
#         "username":request.user.username,
#         "role":profile.role
#     })

class my_profile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

@login_required
def student_issued_book(request):
    if request.user.profile.role != "STUDENT":
        return JsonResponse({"error": "Unauthorized"}, status = 403)
    
    issues = IssuedBook.objects.filter(student = request.user)
    
    result = []

    for issue in issues:
        days = (date.today() - issue.issue_date).days
        fine = (days - 7) * 10 if days > 7 else 0

        result.append({
            "book_name" : issue.book.name,
            "issue_date" : issue.issue_date,
            "fine" : fine
        })

    return JsonResponse(result,safe=False)


class CreateUserView(APIView):
    def post(self,request):
        ser = CreateUserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username= ser.validate_data['username'],
            password=ser.validate_data['password']
        )
        user.profile.role= ser.validate_data['role']
        user.profile.save()

        return Response({"message":"user cretaed"})
    
@method_decorator(csrf_exempt,name='dispatch')
class LoginView(APIView):
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = authenticate(
            username= ser.validated_data['username'],
            password=ser.validated_data['password']
        )



        if not user:
            return Response({"error" : "invalid credatinal"},status = 401)
        
        login(request,user)

        return Response({"message":"login ", "username":user.username,"role":user.profile.role})
    

class AddBookView(APIView):
    permission_classes = [] 


    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Book added successfully"},
                status=200
            )
        return Response(
            serializer.errors,
            status=400
        )