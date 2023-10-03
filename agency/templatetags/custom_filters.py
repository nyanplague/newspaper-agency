from django import template
from django.utils.html import strip_tags
import re

register = template.Library()


@register.filter
def first_two_sentences(content):
    content_stripped = strip_tags(content)
    sentences = re.split(r'(?<=[.!?])\s', content_stripped)

    return ' '.join(sentences[:2])