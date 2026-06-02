from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('lecturer/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('search/', views.search_project, name='search_project'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),
    path('my-project/add/', views.add_student_project, name='add_student_project'),
    path('suggestion/add/', views.add_suggestion, name='add_suggestion'),
    path('suggestion/take/<int:id>/', views.take_suggestion, name='take_suggestion'),
]
