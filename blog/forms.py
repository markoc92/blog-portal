from django import forms
from django.forms import ClearableFileInput
from .models import Comment, Category, Post
from mptt.forms import TreeNodeChoiceField


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('post', 'parent', 'content')

        widgets = {
            'content': forms.Textarea(attrs={'class': 'ml-3 mb-3 form-control border-0 comment-add rounded-0', 'rows': '1', 'placeholder': 'Add a public comment'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)


class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Post Title'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control menudd'})
        self.fields['q'].widget.attrs.update(
            {'data-toggle': 'dropdown'})
        self.fields['q'].required = False


        self.fields['c'].label = 'Category'
        self.fields['c'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['c'].widget.attrs.update(
            {'data-toggle': 'dropdown'})
        self.fields['c'].required = False

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'title', 'image', 'image_caption', 'content', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Category'})
        self.fields['title'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Title', 'name': 'title', 'id': 'id_title'})
        self.fields['image_caption'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Image Caption'})
        self.fields['content'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Content'})
        self.fields['status'].widget.attrs.update({'class': 'form-control mb-3', 'placeholder': 'Status'})

