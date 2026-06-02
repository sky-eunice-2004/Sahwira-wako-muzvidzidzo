from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from .models import Project, Suggestion, StudentProject, UserProfile, Branch, Tag
from .forms import RegisterForm, ProjectForm, SuggestionForm, StudentProjectForm


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name or user.username}! Account created.')
            if role == 'lecturer':
                return redirect('lecturer_dashboard')
            return redirect('student_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            profile = getattr(user, 'profile', None)
            if profile and profile.role == 'lecturer':
                return redirect('lecturer_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def student_dashboard(request):
    profile = getattr(request.user, 'profile', None)
    my_projects = StudentProject.objects.filter(student=request.user).order_by('-created_at')
    suggestions = Suggestion.objects.filter(is_taken=False).order_by('-created_at')[:10]
    taken = Suggestion.objects.filter(taken_by=request.user)
    return render(request, 'student_dashboard.html', {
        'my_projects': my_projects,
        'suggestions': suggestions,
        'taken_suggestions': taken,
    })


@login_required
def lecturer_dashboard(request):
    projects = Project.objects.all().order_by('-created_at')
    my_suggestions = Suggestion.objects.filter(created_by=request.user).order_by('-created_at')
    branches = Branch.objects.all()
    return render(request, 'lecturer_dashboard.html', {
        'projects': projects,
        'my_suggestions': my_suggestions,
        'branches': branches,
    })


def search_project(request):
    query = request.GET.get('q', '').strip()
    projects = None
    not_found = False

    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(branch__name__icontains=query)
        ).distinct()

        if not projects.exists():
            not_found = True
            projects = None

    return render(request, 'search_results.html', {
        'query': query,
        'projects': projects,
        'not_found': not_found,
    })


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()
            # handle tags
            tag_str = form.cleaned_data.get('tags', '')
            if tag_str:
                project.tags.clear()
                for t in tag_str.split(','):
                    t = t.strip().lower()
                    if t:
                        tag_obj, _ = Tag.objects.get_or_create(name=t)
                        project.tags.add(tag_obj)
            messages.success(request, 'Project added successfully!')
            profile = getattr(request.user, 'profile', None)
            if profile and profile.role == 'lecturer':
                return redirect('lecturer_dashboard')
            return redirect('student_dashboard')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


@login_required
def add_student_project(request):
    if request.method == 'POST':
        form = StudentProjectForm(request.POST)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.student = request.user
            sp.save()
            messages.success(request, 'Your project progress saved!')
            return redirect('student_dashboard')
    else:
        form = StudentProjectForm()
    return render(request, 'add_student_project.html', {'form': form})


@login_required
def add_suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.created_by = request.user
            s.save()
            messages.success(request, 'Suggestion added!')
            return redirect('lecturer_dashboard')
    else:
        form = SuggestionForm()
    return render(request, 'add_suggestion.html', {'form': form})


@login_required
def take_suggestion(request, id):
    suggestion = get_object_or_404(Suggestion, id=id)
    if not suggestion.is_taken:
        suggestion.is_taken = True
        suggestion.taken_by = request.user
        suggestion.save()
        messages.success(request, f'You have taken: "{suggestion.title}"')
    else:
        messages.warning(request, 'This suggestion is already taken.')
    return redirect('student_dashboard')


def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    student_entries = StudentProject.objects.filter(project=project)
    return render(request, 'project_detail.html', {
        'project': project,
        'student_entries': student_entries,
    })
