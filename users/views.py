from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Test, TestImage, User, CustomUser
import json

from .forms import CustomUserCreationForm


def home(request):
    user_name = request.user.username

    return render(request, "users/home.html", {'user_name': user_name})


@login_required
def ab_test(request):
    user_role = request.user.role
    test_id = request.GET.get('test_id')
    if test_id:
        if user_role == 'tester':
            test = get_object_or_404(Test, id=test_id, testers=request.user)
        else:
            test = get_object_or_404(Test, id=test_id, user=request.user)
        test_images = test.testimage_set.all()
        test_data = []
        for test_image in test_images:
            test_data.append({
                'image': test_image.image,  # Base64 string
                'rectangles': test_image.rectangles,
                'points': test_image.points
            })
        return render(request, "tests/ab_test.html", {'user_role': user_role, 'test_data': json.dumps(test_data), 'test_id': test_id})
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
    if request.user.role == 'tester':
        tests = request.user.assigned_tests.all()
    else:
        tests = Test.objects.filter(user=request.user)
    return render(request, "tests/my_tests.html", {"tests": tests})


@login_required
def send_test(request):
    testers = User.objects.filter(role='tester')
    return render(request, "tests/send_test.html", {'testers': testers})


@csrf_exempt
@login_required
def submit_test(request):
    if request.method == "POST":
        selected_testers = request.POST.getlist('testers')
        test_id = request.POST.get('test_id')

        try:
            test = Test.objects.get(id=test_id, user=request.user)
            testers = User.objects.filter(id__in=selected_testers, role='tester')
            test.testers.set(testers)
            test.save()
            return JsonResponse({'status': 'success'})
        except Test.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Test not found or you do not have permission'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


class SignUp(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

