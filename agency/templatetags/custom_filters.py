from django import template
from django.utils.html import strip_tags
import nltk

register = template.Library()


@register.filter
def first_two_sentences(content):
    sentences = nltk.sent_tokenize(strip_tags(content))
    return " ".join(sentences[:2])
