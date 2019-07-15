from django.shortcuts import render, redirect
from perfis.models import Perfil, Convite, Post
from django.contrib.auth.decorators import login_required
from perfis.form_post import PostForm
from django.views.generic.base import View


@login_required
def index(request):
    form = PostForm()
    return render(request, 'index.html',
                  {'perfis': Perfil.objects.all(),
                   'perfil_logado': get_perfil_logado(request),
                   'form': form})


@login_required
def exibir(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil in perfil_logado.contatos.all()
    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'perfil_logado': get_perfil_logado(request),
                   'ja_eh_contato': ja_eh_contato})


@login_required
def convidar(request, perfil_id):
    perfil_logado = get_perfil_logado(request)
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    if perfil_a_convidar != perfil_logado:
        perfil_logado.convidar(perfil_a_convidar)
    else:
        print('error')
    return redirect('index')


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()
    return redirect('index')


@login_required
def desfazer_amizade(request, contato_id):
    perfil_logado = get_perfil_logado(request)
    perfil_logado.contatos.remove(contato_id)
    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user.perfil


class PostView(View):
    def post(self, request):
        form = PostForm(request.POST)

        if form.is_valid():
            dados_form = form.cleaned_data
            post = Post()
            post.perfil = get_perfil_logado(request)
            post.postagem = dados_form['postagem']
            post.save()
            return redirect('index')

        return redirect('index')


def add_postaaaaa(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            postagem = form['postagem'].value()
            perfil = get_perfil_logado(request)
            perfil.publicar(postagem)

    return redirect('index')
