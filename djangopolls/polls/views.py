from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

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
    """
        :param request: 각 질문의 상세페이지
        :param question_id: 질문의 pk번호
        :return: pk번호에 해당하는 질문의 투표페이지 
        """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question {}".format(question_id))
