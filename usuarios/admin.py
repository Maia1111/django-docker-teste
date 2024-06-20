from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from .models import Usuario, Unidade
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Formulário personalizado para alterar usuários
class UsuarioChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario

# Formulário personalizado para criar novos usuários com validação de e-mail único
class CustomUserCreationForm(forms.ModelForm):
    senha1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    senha2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ("email", "username", "first_name", "last_name")  # Adicione outros campos conforme necessário

    def clean_senha2(self):
        # Verifique se as duas entradas de senha correspondem
        senha1 = self.cleaned_data.get("senha1")
        senha2 = self.cleaned_data.get("senha2")
        if senha1 and senha2 and senha1 != senha2:
            raise ValidationError("As senhas não correspondem")
        return senha2

    def save(self, commit=True):
        # Salve a senha fornecida em formato hash
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["senha1"])
        if commit:
            usuario.save()
        return usuario

# Admin personalizado para o modelo Usuario
class CustomUserAdmin(UserAdmin):
    form = UsuarioChangeForm
    add_form = CustomUserCreationForm
    model = Usuario
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'unidade', 'foto', 'data_cadastro']
    readonly_fields = ['data_cadastro']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined', 'data_cadastro', 'data_validacao')}),
        ('Outros', {'fields': ('unidade', 'matricula', 'rg', 'cpf', 'foto', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'dados_completos', 'upload_foto', 'mudanca_senha', 'dados_validados', 'usuario_validador')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'senha1', 'senha2'),
        }),
    )

# Registra Usuario com CustomUserAdmin
admin.site.register(Usuario, CustomUserAdmin)

# Registra outros modelos como necessário
admin.site.register(Unidade)