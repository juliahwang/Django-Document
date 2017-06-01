from django.http import HttpResponse
from django.shortcuts import render

from polls.models import Question


# Create your views here.
def index(request):
    """
    :param request: 질문을 모두 보고싶은 경우 
    :return: 모든 질문 리스트
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question {}".format(question_id))


def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question {}".format(question_id))
