from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Suggestion, StudentProject, UserProfile, Tag


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [('student', 'Student'), ('lecturer', 'Lecturer')]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role']


class ProjectForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separated tags e.g. AI, machine learning, python',
        widget=forms.TextInput(attrs={'placeholder': 'AI, machine learning, python'})
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'recommendations', 'status', 'branch']

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            tag_str = self.cleaned_data.get('tags', '')
            if tag_str:
                project.tags.clear()
                for t in tag_str.split(','):
                    t = t.strip().lower()
                    if t:
                        tag_obj, _ = Tag.objects.get_or_create(name=t)
                        project.tags.add(tag_obj)
        return project


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'description', 'branch']


class StudentProjectForm(forms.ModelForm):
    class Meta:
        model = StudentProject
        fields = ['title', 'progress', 'where_stopped', 'project']
        widgets = {
            'progress': forms.Textarea(attrs={'rows': 4}),
            'where_stopped': forms.Textarea(attrs={'rows': 4}),
        }
