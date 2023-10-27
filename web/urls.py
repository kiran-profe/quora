from django.urls import path
from . import views


app_name = 'web'

urlpatterns = [
    path('',views.questions_list,name = 'questions_list'),
    path('ask-question',views.ask_question,name = 'ask_question'),
    path('question-details/<int:id>/',views.question_details,name='question_details'),
    path('question-likes/',views.question_likes,name='question_likes'),
    path('update-question/<int:id>/',views.update_question ,name = 'update_question'),
    path('delete-question/<int:id>/', views.delete_question, name='delete_question'),
    path('comment-reply/<int:id>',views.comment_reply,name = 'comment_reply'),
    path('delete-comment/<int:id>',views.delete_comment,name='delete_comment'),
    path('delete-reply/<int:id>', views.delete_reply, name='delete_reply')

]