from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from agency.forms import (
    NewspaperForm,
    NewspaperSearchForm,
    TopicForm,
    RedactorCreationForm,
    RedactorSearchForm,
    CommentForm,
    RedactorYearsUpdateForm,
)
from agency.models import Newspaper, Topic, Redactor, Commentary


def index(request: HttpRequest) -> HttpResponse:
    newspapers_list = Newspaper.objects.select_related("topic").order_by(
        "publish_date"
    )
    topics_list = Topic.objects.all()

    return render(
        request,
        "agency/index.html",
        context={
            "newspapers_list": newspapers_list,
            "topics_list": topics_list,
        },
    )


class NewspaperListView(generic.ListView):
    model = Newspaper
    paginate_by = 5
    queryset = Newspaper.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["title"] = title
        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        form = NewspaperSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


def newspaper_detail_view(request: HttpRequest, pk) -> HttpResponse:
    newspaper = Newspaper.objects.get(id=pk)

    if request.method == "GET":
        form = CommentForm(initial={"user": request.user})
        context = {"form": form, "newspaper": newspaper}
        return render(request, "agency/newspaper_detail.html", context=context)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if request.user.is_anonymous:
            form.add_error("content", "Please log in to add a comment")
        elif form.is_valid():
            Commentary.objects.create(
                user=request.user, newspaper=newspaper, **form.cleaned_data
            )
            return HttpResponseRedirect(
                reverse("agency:newspaper-detail", kwargs={"pk": pk})
            )

        context = {"form": form, "newspaper": newspaper}

        return render(request, "agency/newspaper_detail.html", context=context)


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")


class TopicDetailView(generic.DetailView):
    model = Topic


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("agency:index")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("agency:index")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic


class RedactorListView(generic.ListView):
    model = Redactor
    queryset = Redactor.objects.all()
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["username"] = username
        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = RedactorSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


def redactor_detail_view(request: HttpRequest, pk: int) -> render:
    redactor = Redactor.objects.filter(id=pk).first()

    if redactor:
        newspapers_list = redactor.newspapers.all()
        paginator = Paginator(newspapers_list, 3)

        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context = {
            "redactor": redactor,
            "newspapers_page": page_obj,
        }

        return render(request, "agency/redactor_detail.html", context=context)
    else:
        return render(request, "agency/redactor_list.html")


class RedactorCreateView(generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsUpdateForm
    success_url = reverse_lazy("agency:redactor-list")


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("agency:redactor-list")
