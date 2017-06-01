from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


# # Create your views here.
### 제너릭 뷰
class IndexView(generic.ListView):
    """
    ListView : 오브젝트 리스트를 보여준다
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """최근 5개의 질문을 리스트로 반환한다"""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    DetailView : 특정 오브젝트의 디테일을 보여준다.
    이 제너릭뷰는 기본적으로 URL 기본키인 'pk'를 전달받아야 하므로 url에서 정규식 이름을 바꿔주었다.
    """
    model = Question  # 어떤 모델을 선택하는가?
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'  # 기본형은 <앱이름>/<모델명_detail.html>이다.
    # 그러나 template_name으로 주면 이름을 변경할 수 있다.


### 일반함수로 구현한 뷰
# def index(request):
#     """
#     :param request: 질문을 모두 보고싶은 경우
#     :return: 모든 질문 리스트
#     """
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     """
#         :param request: 각 질문의 상세페이지
#         :param question_id: 질문의 pk번호
#         :return: pk번호에 해당하는 질문의 투표페이지
#         """
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


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
