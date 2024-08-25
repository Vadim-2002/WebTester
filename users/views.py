import statistics

from django.db.models import Q, Avg, ExpressionWrapper, DurationField, F
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Test, TestImage, User, CustomUser, TestResult, ProfileEditForm
import json

from .forms import CustomUserCreationForm


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            print(user.username)
            user.save()
            return redirect('personal_account')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})


def create_test(request):
    user_name = request.user.username
    return render(request, "tests/create_test.html", {'user_name': user_name})


def personal_account(request):
    user_name = request.user.username
    return render(request, "users/personal_account.html", {'user_name': user_name})


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
            test_name = data.get('name', 'Unnamed Test')
            test_data = data.get('data', [])

            test = Test.objects.create(user=request.user, name=test_name)
            for item in test_data:
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
    user_role = request.user.role
    if user_role == 'tester':
        tests = request.user.assigned_tests.all()
    else:
        tests = Test.objects.filter(user=request.user)
    return render(request, "tests/my_tests.html", {"tests": tests, 'user_role': user_role})


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
            return redirect('ab_test')
        except Test.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Test not found or you do not have permission'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


import datetime


def parse_time_string(time_string):
    minutes, seconds, milliseconds = map(int, time_string.split(':'))
    return datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def format_time_string(time_delta):
    total_seconds = time_delta.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    return f"{int(minutes):02}:{seconds:02}:{milliseconds:03}"


def calculate_time_statistics(time_strings):
    time_deltas = [parse_time_string(ts) for ts in time_strings]

    # Среднее время
    total_time = sum(time_deltas, datetime.timedelta())
    average_time = total_time / len(time_deltas)

    # Максимальное и минимальное время
    max_time = max(time_deltas)
    min_time = min(time_deltas)

    # Медиана
    median_time = statistics.median(time_deltas)

    return {
        'average': format_time_string(average_time),
        'max': format_time_string(max_time),
        'min': format_time_string(min_time),
        'median': format_time_string(median_time),
    }

@login_required
def test_results_detail(request):
    test = get_object_or_404(Test, id=request.GET.get('test_id'))
    if test.user.id == request.user.id:
        test_results = TestResult.objects.filter(test=test)
    else:
        test_results = TestResult.objects.filter(test=test, tester=request.user.id)

    # подсчет среднего времени прохождения теста по всем тестировщикам
    all_time = []
    for result in test_results:
        all_time.append(result.duration)

    statistic_by_test = calculate_time_statistics(all_time)
    average_time = calculate_time_statistics(all_time)['average']

    context = {
        'test': test,
        'test_results': test_results
    }

    context.update(statistic_by_test)

    return render(request, 'tests/test_results_detail.html', context)


@csrf_exempt
def save_test_results(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            start_time = data.get('start_time')
            end_time = data.get('end_time')
            test_id = data.get('test_id')

            # Преобразование строк в объекты datetime
            start_time = timezone.datetime.fromisoformat(start_time)
            end_time = timezone.datetime.fromisoformat(end_time)

            test = get_object_or_404(Test, id=test_id)

            # Создание объекта результата теста и сохранение его в базу данных
            test_result = TestResult(
                test=test,
                start=start_time,
                end=end_time,
                tester=request.user
            )
            test_result.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def delete_test(request):
    test_id = request.GET.get('test_id')
    test = get_object_or_404(Test, id=test_id)

    if request.method == 'GET':
        if request.user == test.user:
            test.delete()
            return redirect('my_tests')
        else:
            return redirect('my_tests')

    return redirect('my_tests')


class SignUp(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

