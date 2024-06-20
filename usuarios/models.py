from django.db import models
from django.contrib.auth.models import AbstractUser



class Unidade(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    endereco = models.CharField(max_length=100)
    email = models.EmailField()    


    def __str__(self):
        return self.sigla





class Usuario(AbstractUser): 

    
    choices_nivel_usuario =(
        ('1', 'Bronze'),
        ('2', 'Prata'),
        ('3', 'Ouro')
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)    
    unidade = models.ForeignKey(Unidade, on_delete=models.DO_NOTHING, null=True, blank=True)
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rg = models.CharField(max_length=50, unique=True, null=True, blank=True)
    cpf = models.CharField(max_length=50, unique=True, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos', null=True, blank=True)
    telefone = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    rua = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)  # Adicione unique=True 
    dados_completos = models.BooleanField(default=False)
    upload_foto = models.BooleanField(default=False)
    mudanca_senha = models.BooleanField(default=False)
    nivel_usuario = models.CharField(max_length=1, choices=choices_nivel_usuario, default='1')
    dados_validados = models.BooleanField(default=False)
    usuario_validador = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='validador')
    data_validacao = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.username