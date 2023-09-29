from django import forms

from .models import *


form_control = {'class': 'form-select'}

text_attrs = {'type': 'text', 'class': 'form-control'}
text_box_attrs = {'type': 'text', 'class': 'form-control', 'cols': 70}
file_attrs = {'type': 'file', 'class': 'form-control'}

date_attrs = {'type': 'date', 'class': 'form-control'}
number_attrs = {'type': 'number', 'class': 'form-control'}
year_attrs = {'type': 'number', 'class': 'form-control'}

comment_attrs = {'type': 'text', 'class': 'form-control', 'cols': 70, 'rows': 1, 'placeholder': 'Add your comment'}


class PersonForm(forms.ModelForm):
    class Meta:
        abstract = True
        fields = ('name', 'bio', 'photo', 'slug')

        widgets = {
            'name': forms.TextInput(attrs=text_attrs),
            'bio': forms.Textarea(attrs=text_box_attrs),
            'photo': forms.FileInput(attrs=file_attrs),
            'slug': forms.TextInput(attrs=text_attrs),
        }


class ActorForm(PersonForm):

    class Meta:
        model = Actor
        fields = PersonForm.Meta.fields

        widgets = PersonForm.Meta.widgets


class DirectorForm(PersonForm):

    class Meta:
        model = Director
        fields = PersonForm.Meta.fields

        widgets = PersonForm.Meta.widgets


class MovieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'about', 'year', 'country', 'world_premiere', 'poster', 'video',
                  'actors', 'directors', 'genres', 'rating', 'budget', 'fees', 'slug')

        widgets = {
            'title': forms.TextInput(attrs=text_attrs),
            'tagline': forms.TextInput(attrs=text_attrs),
            'about': forms.Textarea(attrs=text_box_attrs),
            'year': forms.NumberInput(attrs=number_attrs),
            'country': forms.TextInput(attrs=text_attrs),
            'world_premiere': forms.DateInput(attrs=date_attrs),
            'poster': forms.FileInput(attrs=file_attrs),
            'video': forms.FileInput(attrs=file_attrs),
            'actors': forms.SelectMultiple(attrs=form_control),
            'directors': forms.SelectMultiple(attrs=form_control),
            'genres': forms.SelectMultiple(attrs=form_control),
            'rating': forms.NumberInput(attrs=number_attrs),
            'budget': forms.NumberInput(attrs=number_attrs),
            'fees': forms.NumberInput(attrs=number_attrs),
            'slug': forms.TextInput(attrs=text_attrs)
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description', 'slug')

        widgets = {
            'name': forms.TextInput(attrs=text_attrs),
            'description': forms.Textarea(attrs=text_box_attrs),
            'slug': forms.TextInput(attrs=text_attrs)
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs=comment_attrs)
        }
