from django.test import TestCase

from agency.forms import RedactorSearchForm, NewspaperSearchForm


class FormsTests(TestCase):
    def test_redactor_search_form_is_valid(self):
        form_data = {"username": "test_username"}
        form = RedactorSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_newspaper_search_form_is_valid(self):
        form_data = {"title": "test_title"}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)
