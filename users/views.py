import base64

from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Test, TestImage
import json

from .forms import CustomUserCreationForm


def home(request):
    return render(request, "users/home.html")


def ab_test(request):
    user_role = request.user.role
    test_id = request.GET.get('test_id')
    if test_id:
        test = get_object_or_404(Test, id=test_id, user=request.user)
        test_images = test.testimage_set.all()
        test_data = []
        for test_image in test_images:
            test_data.append({
                'image': test_image.image,
                'rectangles': test_image.rectangles,
                'points': test_image.points
            })
        return render(request, "tests/ab_test.html", {'user_role': user_role, 'test_data': json.dumps(test_data)})
    return render(request, "tests/ab_test.html", {'user_role': user_role})


@csrf_exempt
def save_test(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            test = Test.objects.create(user=request.user)
            for item in data:
                image = item['image']
                rectangles = item['rectangles']
                points = item['points']
                TestImage.objects.create(test=test, image=image, rectangles=rectangles, points=points)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def my_tests(request):
    tests = Test.objects.filter(user=request.user)
    return render(request, "tests/my_tests.html", {"tests": tests})


@csrf_exempt
@login_required
def load_test(request, test_id):
    if request.method == "GET":
        test = get_object_or_404(Test, id=test_id, user=request.user)
        test_images = TestImage.objects.filter(test=test)
        data = [{
            'image': img.image,
            'rectangles': img.rectangles,
            'points': img.points
        } for img in test_images]
        return JsonResponse({'status': 'success', 'data': data})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

