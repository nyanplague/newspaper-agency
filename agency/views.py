from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperForm, NewspaperSearchForm, TopicForm
from agency.models import Newspaper, Topic


def index(request: HttpRequest) -> HttpResponse:
    newspapers_list = Newspaper.objects.select_related("topic").order_by("publish_date")
    topics_list = Topic.objects.all()

    return render(
        request,
        "agency/index.html",
        context={"newspapers_list": newspapers_list, "topics_list": topics_list},
    )


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["title"] = title
        context["search_form"] = NewspaperSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class TopicDetailView(generic.DetailView):
    model = Topic


class TopicCreateView(generic.CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("agency:index")


class TopicDeleteView(generic.DeleteView):
    model = Topic

