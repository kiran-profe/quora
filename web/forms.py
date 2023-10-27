from django import forms
from .models import Question, Comment


class QuestionAskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title' , 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class QuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title','body']