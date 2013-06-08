from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone

from polls.models import Choice, Poll


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        #polls = Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        polls = Poll.objects.filter(pub_date__lte=timezone.now())
        return polls


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


@login_required
def vote(request, poll_id):

    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.voted_user = request.user
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. all the votes they gaThis prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


@login_required
def user_page(request):
    questions = Poll.objects.filter(user=request.user)

    voted_polls = []
    choices = Choice.objects.filter(voted_user=request.user)
    for choice in choices:
        voted_polls.append(Poll.objects.get(id=choice.poll.id))
    voted_polls = list(set(voted_polls))

    context = {'questions': questions,
               'voted_polls': voted_polls}
    return render(request,
                  'polls/user_page.html',
                  context)


@login_required
def delete(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.user == poll.user:
        poll.delete()
    return HttpResponseRedirect(reverse('polls:user_page'))


@login_required
def change(request, poll_id):
    if request.method == "GET":
        poll = Poll.objects.get(id=poll_id)
        choices = Choice.objects.filter(poll=poll)
        form = ChangeVotedPollForm(choices)
        context = {'poll': poll, 'choices': choices, 'form': form}
        return render(request,
                      'polls/user_page.html',
                      context)
    if request.method == "POST":
        return HttpResponseRedirect(reverse('polls:user_page'))
