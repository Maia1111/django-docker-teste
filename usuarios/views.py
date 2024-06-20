import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from .models import Usuario, Unidade


@csrf_protect
@login_required
def criar_usuario(request):
    unidades = Unidade.objects.all()
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))

    if request.method == "GET":
        return render(request, 'criar_usuario.html', {'unidades': unidades})

    if request.method == "POST":
        nome = request.POST.get('nome', '').strip().upper()
        sobrenome = request.POST.get('sobrenome', '').strip().upper()
        usuario = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        unidade_id = request.POST.get('unidade', '').strip()

        if not nome:
            messages.add_message(request, messages.ERROR, 'Nome é obrigatório')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        if not sobrenome:
            messages.add_message(request, messages.ERROR, 'Sobrenome é obrigatório')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        if not usuario:
            messages.add_message(request, messages.ERROR, 'Usuário é obrigatório')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        if Usuario.objects.filter(username=usuario).exists():
            messages.add_message(request, messages.ERROR, 'Usuário já cadastrado')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        if not email:
            messages.add_message(request, messages.ERROR, 'Email é obrigatório')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        if Usuario.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email já cadastrado')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        try:
            unidade = Unidade.objects.get(id=unidade_id)
        except Unidade.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Unidade inválida')
            return render(request, 'criar_usuario.html', {'unidades': unidades})

        user = Usuario.objects.create_user(
            first_name=nome,
            last_name=sobrenome,  # Certifique-se de que está passando o sobrenome corretamente
            username=usuario,
            password=senha,
            email=email,
            unidade=unidade
        )
        user.save()

        # Envia o email
        remetente = settings.DEFAULT_FROM_EMAIL
        assunto = 'Informações de Login'
        mensagem = f"""
        Olá {user.first_name},

        Seguem suas informações de login inicial:

        Usuário: {usuario}
        Senha: {senha}

        Faça o login em: {settings.BASE_URL}/login


       
        Atenciosamente,
        Nexus Scorpions
        """
        
        destinatario = email  # Este é o email do usuário que acabou de se cadastrar

        try:
            send_mail(
                assunto,
                mensagem,
                remetente,
                [destinatario],
                fail_silently=False,
            )
            messages.add_message(request, messages.SUCCESS, 'Usuário criado com sucesso')
            return redirect(reverse('criar_usuario'))

        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Falha ao enviar email')
            return redirect(reverse('criar_usuario'))

    return render(request, 'criar_usuario.html', {'unidades': unidades})


@csrf_protect
def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')

    if request.method == "POST":
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        
       
        user = authenticate(username=usuario, password=senha)
        

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login.html')
        


        if not user.dados_completos:
            login(request, user)            
            messages.add_message(request, messages.INFO, 'Complete seus dados para continuar')
        
            return redirect(reverse('completar_dados'))

        if not user.upload_foto:         
            messages.add_message(request, messages.INFO, 'Agora faça o upload de sua foto')
            return redirect(reverse('upload_foto'))

        if not user.mudanca_senha: 
            if user is not None:
                login(request, user)          
            messages.add_message(request, messages.INFO, 'Quase lá, mude sua senha inicial')

            return redirect(reverse('mudar_senha'))
        

        if not user.dados_validados:           
            return render(request, 'aguarde_validacao.html')

        login(request, user)
        return redirect(reverse('home'))  


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('login_view'))  


@login_required
def completar_dados(request):
    if request.method == "GET":
        return render(request, 'completar_dados.html')

    if request.method == "POST":
        usuarios = Usuario.objects.all()
        user = Usuario.objects.get(username=request.user.username)
        matricula = request.POST.get('matricula', '').strip()
        rg = request.POST.get('rg', '').strip()
        cpf = request.POST.get('cpf', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        cep = request.POST.get('cep', '').strip()
        rua = request.POST.get('rua', '').strip()
        numero = request.POST.get('numero', '').strip()
        bairro = request.POST.get('bairro', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        estado = request.POST.get('estado', '').strip()

        if not matricula:
            messages.add_message(request, messages.ERROR, 'Matricula é obrigatória')
            return render(request, 'completar_dados.html')

        if not rg:
            messages.add_message(request, messages.ERROR, 'RG é obrigatório')
            return render(request, 'completar_dados.html')

        if not cpf:
            messages.add_message(request, messages.ERROR, 'CPF é obrigatório')
            return render(request, 'completar_dados.html')

        if not cep:
            messages.add_message(request, messages.ERROR, 'CEP é obrigatório')
            return render(request, 'completar_dados.html')

        if not telefone:
            messages.add_message(request, messages.ERROR, 'Telefone é obrigatório')
            return render(request, 'completar_dados.html')

        if not rua:
            messages.add_message(request, messages.ERROR, 'Rua é obrigatória')
            return render(request, 'completar_dados.html')

        if not numero:
            messages.add_message(request, messages.ERROR, 'Número é obrigatório')
            return render(request, 'completar_dados.html')

        if not bairro:
            messages.add_message(request, messages.ERROR, 'Bairro é obrigatório')
            return render(request, 'completar_dados.html')

        if not cidade:
            messages.add_message(request, messages.ERROR, 'Cidade é obrigatória')
            return render(request, 'completar_dados.html')

        if not estado:
            messages.add_message(request, messages.ERROR, 'Estado é obrigatório')
            return render(request, 'completar_dados.html')

        if usuarios.filter(matricula=matricula).exists():
            messages.add_message(request, messages.ERROR, 'Matricula já cadastrada')
            return render(request, 'completar_dados.html')

        if usuarios.filter(rg=rg).exists():
            messages.add_message(request, messages.ERROR, 'RG já cadastrado')
            return render(request, 'completar_dados.html')

        if usuarios.filter(cpf=cpf).exists():
            messages.add_message(request, messages.ERROR, 'CPF já cadastrado')
            return render(request, 'completar_dados.html')

        user.matricula = matricula
        user.rg = rg
        user.cpf = cpf
        user.telefone = telefone
        user.rua = rua
        user.cep = cep
        user.numero = numero
        user.bairro = bairro
        user.cidade = cidade
        user.estado = estado
        user.dados_completos = True
        user.save()
        messages.add_message(request, messages.INFO, 'Falta pouco, faça o upload de sua foto')
        return redirect(reverse('upload_foto'))
    

@login_required
def upload_foto(request):
    if request.method == "GET":
        return render(request, 'upload_foto.html')

    if request.method == "POST":
        user = Usuario.objects.get(username=request.user.username)
        foto = request.FILES.get('foto')

        if not foto:
            messages.add_message(request, messages.ERROR, 'Foto é obrigatória')
            return render(request, 'upload_foto.html')

        user.foto = foto
        user.upload_foto = True
        user.save()
        return redirect(reverse('mudar_senha'))
    

@login_required
def mudar_senha(request):
    if request.method == "GET":
        return render(request, 'mudar_senha.html')

    if request.method == "POST":
        user = Usuario.objects.get(username=request.user.username)
        senha = request.POST.get('senha', '').strip()
        confirmar_senha = request.POST.get('confirmar_senha', '').strip()

        if not senha:
            messages.add_message(request, messages.ERROR, 'Senha é obrigatória')
            return render(request, 'mudar_senha.html')

        if not confirmar_senha:
            messages.add_message(request, messages.ERROR, 'Confirmação de senha é obrigatória')
            return render(request, 'mudar_senha.html')

        if senha != confirmar_senha:
            messages.add_message(request, messages.ERROR, 'As senhas não correspondem')
            return render(request, 'mudar_senha.html')

        try:
            user.set_password(senha)
            user.mudanca_senha = True
            user.save()

            # Verifique se o valor foi salvo corretamente
            user.refresh_from_db()
            if user.mudanca_senha:
                print("mudanca_senha foi salvo como True")

                # enviar email para o usuário
                assunto = 'Mudança de Senha'
                mensagem = f"""
                Olá {user.first_name},
               

                Sua senha foi alterada com sucesso.
                Por favor, mantenha esta informação em segurança.
                Assim que for validado seu cadastro, você receberá um email de confirmação e poderá entrar no sistema.

                {settings.BASE_URL}/login


                Atenciosamente,
                Nexus Scorpions
                """
                remetente = settings.DEFAULT_FROM_EMAIL

              
                send_mail(
                        assunto,
                        mensagem,
                        remetente,
                        [user.email],
                        fail_silently=False,
                    )                          
                return redirect(reverse('aguarde_validacao'))
        except Exception as e:
                    print(f"Erro ao enviar email: {e}")
                    messages.add_message(request, messages.ERROR, 'Falha ao enviar email')
                    return redirect(reverse('mudar_senha'))
        
       
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Usuario

def home(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Você não está logado')
        return redirect(reverse('login_view'))

    try:
        user = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        return redirect(reverse('login_view'))

    if not user.dados_validados:
        messages.add_message(request, messages.ERROR, 'Complete seus dados para continuar')
        return redirect(reverse('completar_dados'))

    return render(request, 'home.html', {'usuario': user})


    
@login_required
def admin_usuarios(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))
    
    usuarios = Usuario.objects.all()
    return render(request, 'admin_usuarios.html', {'usuarios': usuarios})
    
   
def aguarde_validacao(request):       
    return render(request, 'aguarde_validacao.html')


def recuperacao_senha(request):
    """Permite a recuperação de senha através do email."""
    if request.method == "GET":
        return render(request, 'recuperacao_senha.html')

    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        confirmar_email = request.POST.get('confirmar_email', '').strip()

        if not email:
            messages.add_message(request, messages.ERROR, 'Email é obrigatório')
            return render(request, 'recuperacao_senha.html')

        if not confirmar_email:
            messages.add_message(request, messages.ERROR, 'Confirmação de email é obrigatória')
            return render(request, 'recuperacao_senha.html')

        if email != confirmar_email:
            messages.add_message(request, messages.ERROR, 'Os emails não correspondem')
            return render(request, 'recuperacao_senha.html')

        if not Usuario.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email não cadastrado')
            return render(request, 'recuperacao_senha.html')

        user = Usuario.objects.get(email=email)
        nova_senha = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        user.set_password(nova_senha)       
        user.save()

        assunto = 'Recuperação de Senha'
        mensagem = f"""
        Olá {user.first_name},
       

        Seu usuário é: {user.username}
        Sua nova senha é: {nova_senha}

      
        Faça o login em: {settings.BASE_URL}/login



        Caso deseje, altere sua senha na plataforma.
       

        Por favor, mantenha esta informação em segurança.

        Atenciosamente,
        Nexus Scorpions
        """
        remetente = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(
                assunto,
                mensagem,
                remetente,
                [email],
                fail_silently=False,
            )
            return redirect(reverse('mensagem_recuperacao_senha'))
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            messages.add_message(request, messages.ERROR, 'Falha ao enviar email')
            return redirect(reverse('recuperacao_senha'))
        

def mensagem_recuperacao_senha(request):
    """Exibe uma mensagem de sucesso após a recuperação da senha."""
    return render(request, 'mensagem_recuperacao_senha.html')


@login_required
def listar_usuarios_validar(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))
    usuarios = Usuario.objects.all().filter(mudanca_senha=True).filter(dados_completos=True).filter(upload_foto=True).filter(dados_validados=False)

    return render(request, 'lista_validacao_usuarios.html', {'usuarios': usuarios})


def ver_detalhe_usuario_validar(request, id):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))
    usuario = get_object_or_404(Usuario, id=id)
    return render(request, 'detalhe_usuario_validar.html', {'usuario': usuario})


@login_required
def validar_usuario(request, id):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))
    usuario = get_object_or_404(Usuario, id=id)

    
    if  not usuario.dados_validados:
        try:
            usuario.dados_validados = True
            usuario.usuario_validador = request.user
            usuario.data_validacao = timezone.now()
            usuario.save()
            messages.add_message(request, messages.SUCCESS, 'Usuário validado com sucesso')

            # enviar email para o usuário

            assunto = 'Validação de Cadastro'
            mensagem = f"""
            Olá {usuario.first_name},
        

            Seus dados foram validados com sucesso.
            Agora você pode acessar o sistema com seu usuário e senha no sistema.

            Faça o login em: {settings.BASE_URL}/login


            Atenciosamente,
            Nexus Scorpions
            """
            remetente = settings.DEFAULT_FROM_EMAIL

                
            send_mail(
                    assunto,
                    mensagem,
                    remetente,
                    [usuario.email],
                    fail_silently=False,
                )
            
            return redirect(reverse('usuarios_validados'))
        except Exception as e:
            print(f"Erro ao validar usuário: {e}")
            messages.add_message(request, messages.ERROR, 'Erro ao validar usuário')
            return redirect(reverse('listar_usuarios_validar'))
    else:
        messages.add_message(request, messages.ERROR, 'Usuário já validado')
        return redirect(reverse('usuarios_validados'))


@login_required
def usuarios_validados(request):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')
        return redirect(reverse('login_view'))
    
    usuarios = Usuario.objects.all().filter(dados_validados=True).order_by('-data_validacao')
    return render(request, 'lista_usuarios_validados.html', {'usuarios': usuarios})


@login_required
def rejeitar_validacao(request, id):
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Você não tem permissão para acessar esta página')        
        return redirect(reverse('login_view'))
    
    usuario = get_object_or_404(Usuario, id=id)
   


   # enviar email para o usuário

    assunto = 'Validação de Cadastro'
    mensagem = f"""
    Olá {usuario.first_name},
   

    Seus dados foram analisados e precisam ser revisados e enviados novamente para análise.
    Por favor, entre novamente no sistema, revise e corrija  seus dados e envie novamente.

    {settings.BASE_URL}/login

    Atenciosamente,
    Nexus Scorpions
    """
    remetente = settings.DEFAULT_FROM_EMAIL

    try:
        usuario.dados_completos = False
        usuario.upload_foto = False 
        usuario.mudanca_senha = False  
        usuario.dados_validados = False
        usuario.usuario_validador = None
        usuario.data_validacao = None
        usuario.cpf = None
        usuario.rg = None
        usuario.matricula = None
        usuario.telefone = None
        usuario.rua = None
        usuario.cep = None
        usuario.numero = None
        usuario.bairro = None
        usuario.cidade = None
        usuario.estado = None
        usuario.foto = None
        usuario.save()       
    
        send_mail(
            assunto,
            mensagem,
            remetente,
            [usuario.email],
            fail_silently=False,
        )
       
        messages.add_message(request, messages.SUCCESS, 'Dados de usuario invalidado com sucesso!')
        return redirect(reverse('listar_usuarios_validar'))
    except Exception as e:
        print(f"Erro ao invalidar usuário: {e}")
        messages.add_message(request, messages.ERROR, 'Erro  ao invalidar usuário')
        return redirect(reverse('listar_usuarios_validar'))