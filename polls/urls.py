from django.urls import path, include

from . import views

urlpatterns = [
    path('v1/', include([
        # List views
        path('poll/', views.PollView.as_view()),
        path('question/', views.QuestionView.as_view()),
        path('answer/', views.AnswerView.as_view()),

        # Polling views
        path('polling/', views.QuestionPollingView.as_view()),

        path('results/', views.PassedPollsView.as_view()),

        # Admin views
        path('admin/', include([
            path(r'poll/', views.AdminPollView.as_view()),
            path(r'question/', views.AdminQuestionView.as_view()),
        ])),
        path('auth/', include('rest_auth.urls')),
    ]))
]