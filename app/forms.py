from django import forms
from django.contrib.auth.models import User 
from .models import Usuario, Feedback, Venda, Fornecedor, Produto, ItensdeVenda,ItemCarrinho,Estoque



class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'endereco', 'telefone', 'cidade']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentarios', 'avaliacoes', 'usuario']
        widgets = {
            'comentarios': forms.TextInput(attrs={'class': 'form-control'}),
            'avaliacoes': forms.Select(attrs={'class': 'form-control'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['nome', 'tipovenda', 'valor', 'quantidade', 'pagamento', 'datavenda', 'usuario']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipovenda': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'pagamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'datavenda': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'CPF', 'email', 'endereco', 'telefone', 'cidade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'CPF': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo', 'preco', 'quantidade', 'imagem', 'idfornecedor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'idfornecedor': forms.Select(attrs={'class': 'form-control'}),
        }


class AdicionarItemCarrinhoForm(forms.ModelForm):
    produto = forms.ModelChoiceField(queryset=Produto.objects.all(), empty_label="Escolha um produto")
    quantidade = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = ItemCarrinho
        fields = ['produto', 'quantidade']


class ItensdeVendaForm(forms.ModelForm):
    class Meta:
        model = ItensdeVenda
        fields = ['produto', 'preco', 'quantidade', 'categoria', 'disponibilidade_estoque', 'idvendas']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponibilidade_estoque': forms.TextInput(attrs={'class': 'form-control'}),
            'idvendas': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','password']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
            'username': forms.TextInput(attrs={'placeholder': 'Digite seu nome de usuario'}),
        }

class CadastroForm(forms.ModelForm):
    confirmacao_senha = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}), required=True)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'endereco', 'telefone', 'cidade']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmacao_senha = cleaned_data.get('confirmacao_senha')

        if password and confirmacao_senha and password != confirmacao_senha:
            self.add_error('confirmacao_senha', 'As senhas não coincidem.')

    
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }    
    


