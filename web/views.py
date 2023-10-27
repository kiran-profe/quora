from django.shortcuts import render
from .models import Question, Comment, Replies
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuestionAskForm, CommentForm, QuestionUpdateForm
from django.shortcuts import render , get_object_or_404 , Http404
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse


def questions_list(request):

    questions = Question.objects.all().order_by('-created')
    context = {
        'questions' : questions
    }

    return render(request , 'web/questions_list.html' , context = context)


@login_required()
def ask_question(request):

    if request.method == 'POST':
        form = QuestionAskForm(request.POST)

        if form.is_valid():
            ques = form.save(commit=False)
            ques.author = request.user
            ques.save()

            return HttpResponseRedirect(reverse('web:questions_list'))
    else:
        form = QuestionAskForm()

    context = {
        'form' : form
    }

    return render(request , 'web/ask_question.html',context)


def question_details(request,id):

    question = get_object_or_404(Question,id=id)

    replies = Replies.objects.all().filter(question = question).order_by('-timestamp')

    is_liked = False
    if question.likes.filter(id = request.user.id).exists():
        is_liked = True

    is_favourite = False

    comments =  Comment.objects.all().filter(question = question).order_by('-timestamp')

    if request.method == 'POST':

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('user:login'))

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            cmnt = comment_form.save(commit=False)
            cmnt.user = request.user
            cmnt.question = question
            cmnt.save()
            return HttpResponseRedirect(reverse('web:question_details',args = (id,)))
    else:
        comment_form  = CommentForm()

    context = {
        'question': question,
        'is_liked' : is_liked,
        'is_favourite' : is_favourite,
        'likes_count' : question.likes.count() ,
        'comments' : comments,
        'comment_form' : comment_form ,
        'replies' : replies,
    }

    return render(request, 'web/question_detail.html', context=context)


def question_likes(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))

    question = get_object_or_404(Question,id = request.POST.get('question_id'))

    if question.likes.filter(id = request.user.id).exists():
        question.likes.remove(request.user)
    else:
        question.likes.add(request.user)

    return HttpResponseRedirect(reverse('web:question_details',args=(request.POST.get('question_id'),)))


@login_required()
def update_question(request,id):

    question = get_object_or_404(Question,id=id)

    if question.author != request.user:
        return Http404()

    if request.method == 'POST':
        form = QuestionUpdateForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web:question_details',args=(id,)))
    else:
        form = QuestionUpdateForm(instance=question)

    context = {
        'form' : form ,
        'question' : question ,
    }

    return render(request ,'web/update_question.html',context)


def delete_question(request,id):

    question = get_object_or_404(Question,id=id)

    if question.author != request.user:
        return Http404()

    if request.method =='POST':
        question.delete()
        return HttpResponseRedirect(reverse('web:questions_list'))

def comment_reply(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))

    text = request.POST.get('text')

    if len(text)==0:
        messages.success(request,'TextField is empty')
        return HttpResponseRedirect(reverse('web:question_details', args=(id,)))

    question = get_object_or_404(Question, id=id)

    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.filter(id=comment_id).first()
    Replies.objects.create(question = question,comment=comment,user = request.user,content =text)

    return HttpResponseRedirect(reverse('web:question_details',args=(id,)))

def delete_comment(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))

    cmnt_id = request.POST.get('comment_id')
    cmnt = get_object_or_404(Comment,id=cmnt_id)

    if cmnt.user != request.user:
        return Http404()
    cmnt.delete()
    return HttpResponseRedirect(reverse('web:question_details', args=(id,)))
    

def delete_reply(request, id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:login'))

    reply_id = request.POST.get('reply_id')
    reply = get_object_or_404(Replies, id=reply_id)

    if reply.user != request.user:
        return Http404()
    reply.delete()
    return HttpResponseRedirect(reverse('web:question_details', args=(id,)))