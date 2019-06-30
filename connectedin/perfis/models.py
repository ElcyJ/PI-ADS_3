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