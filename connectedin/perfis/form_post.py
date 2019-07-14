from django import forms


class PostForm(forms.Form):
    postagem = forms.CharField(label='postagem', max_length=1000)

