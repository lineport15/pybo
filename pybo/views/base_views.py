from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question

def index(request):
    """
    Listing
    """

    #입력 패러미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '') #두번째 인자는 Default값
    so = request.GET.get('so', 'recent')

    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    #question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw)
                ).distinct()

    paginator = Paginator(question_list, 10) #한 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj, 'page': page, 'kw': kw, 'so': so}

    return render(request, 'pybo/question_list.html', context)
#    return HttpResponse("Helelo Pybo!")

def detail(request, question_id):
    """
    Detail
    """

    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
