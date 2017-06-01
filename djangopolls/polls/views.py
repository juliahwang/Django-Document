from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_chice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a chice.",
        })
    else:
        selected_chice.votes += 1
        selected_chice.save()
        # POST 데이터 처리를 정상적으로 마친 뒤에는 항상 HttpResponseRedirect를 리턴
        # 유저가 뒤로 가기를 눌렀을 때 데이터가 두번 저장되는 것을 방지한다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # HttpResponseRedirect를 사용하는 것은 장고 뿐만 아니라 모든 웹개발에 사용된다.
