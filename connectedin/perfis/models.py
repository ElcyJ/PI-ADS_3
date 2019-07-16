from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self')

    usuario_id = models.OneToOneField(User, related_name='perfil',
                                   on_delete=models.CASCADE)

    @property
    def email(self):
        return self.usuario_id.email

    def convidar(self, perfil_convidado):
        Convite(solicitante=self, convidado=perfil_convidado).save()

    @property
    def posts(self):
        return Post.objects.filter(id=self.id)

    @property
    def timeline(self):
        lista_postagens = []
        postagens_ordenadas = Post.objects.all()[::-1]

        for i in postagens_ordenadas:
            if i.perfil in self.contatos.all() or i.perfil.id == self.id:
                lista_postagens.append(i)

        return lista_postagens

    @property
    def superuser(self):
        return self.usuario_id.is_superuser


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE,
                                    related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, on_delete=models.CASCADE,
                                  related_name='convites_recebidos')

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()

    def recusar(self):
        self.delete()


class Post(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='perfil_postagem')
    data_postagem = models.DateTimeField(auto_now_add=True)
    postagem = models.CharField(max_length=255)

    def __str__(self):
        return self.postagem



