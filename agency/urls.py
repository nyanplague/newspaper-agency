from django.urls import path

from agency.views import (index, NewspaperDetailView, NewspaperListView, NewspaperCreateView,
                          TopicDetailView, TopicCreateView, TopicDeleteView)

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperCreateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperCreateView.as_view(), name="newspaper-delete"),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic-detail"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),

]

app_name = "agency"

