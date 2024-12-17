from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.views import View
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout

from django.utils import timezone


#Index################################################################################################################
class IndexView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        produtos = Produto.objects.all()
        if query:
            produtos_filtrados = Produto.objects.filter(nome__icontains=query)
        else:
            produtos_filtrados = produtos

        user = request.user if request.user.is_authenticated else None

        return render(request, 'index.html', {
            'produtos': produtos,
            'produtos_filtrados': produtos_filtrados,
            'query': query,
            'user': user
        })




#Login################################################################################################################
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'usuario/login.html') 

    def post(self, request):
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        print(f"Username: {username}, Senha: {senha}")  
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            auth_login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('login')  

        
#Logout################################################################################################################

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('login')


        
#Cadastro################################################################################################################

class CadastroView(View):
    def get(self, request, *args, **kwargs):
        form = CadastroForm()
        return render(request, 'usuario/cadastro.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CadastroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar usuário: {e}')
                return render(request, 'usuario/cadastro.html', {'form': form})
        else:
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados.')
            return render(request, 'usuario/cadastro.html', {'form': form})

#Perfil################################################################################################################      
class PerfilView(View):
    def get(self, request, id, *args, **kwargs):
        perfil = get_object_or_404(Usuario, id=id)
        form = UsuarioForm(instance=perfil)
        return render(request, 'usuario/perfil.html', {'user': perfil, 'form': form})

class AdicionarPerfilView(View): 
    def get(self, request, *args, **kwargs):
        form = UsuarioForm()
        return render(request, 'usuario/adicionarperfil.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil adicionado com sucesso!')
            return redirect('perfil', id=form.instance.id)
        else:
            return render(request, 'usuario/adicionarperfil.html', {'form': form})    
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Usuario
from .forms import UsuarioForm

class ModificarPerfilView(View):
    def get(self, request, id, *args, **kwargs):
        perfil = get_object_or_404(Usuario, id=id)
        form = UsuarioForm(instance=perfil)
        return render(request, 'usuario/modificarperfil.html', {'form': form})

    def post(self, request, id, *args, **kwargs):
        perfil = get_object_or_404(Usuario, id=id)
        form = UsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            if form.cleaned_data['password']:
                perfil.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request, 'Perfil modificado com sucesso!')
            return redirect('perfil', id=perfil.id)
        else:
            return render(request, 'usuario/modificarperfil.html', {'form': form})


class ExcluirPerfilView(View):
    def get(self, request, id, *args, **kwargs):
        perfil = get_object_or_404(Usuario, id=id)
        perfil.delete()
        messages.success(request, 'Perfil excluído com sucesso!')
        return redirect('perfil')

         
       
#Feedback################################################################################################################       
class FeedbackView(View):
    def get(self,request, *args, **kwargs):
        feedbacks = Feedback.objects.all()
        return render (request, 'feedback/feedback.html',{'feedbacks':feedbacks})
    
class AdicionarFeedbackView(View): 
    def get(self,request, *args, **kwargs):
        form = FeedbackForm()
        return render (request, 'feedback/adicionarfeedback.html',{'form':form})
    def post(self,request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Feedback')
        else:
            return render (request, 'feedback/adicionarfeedback.html',{'form':form})

class ModificarFeedbackView(View):
    def get(self,request,id, *args, **kwargs):
        feedback = get_object_or_404(Feedback, id=id)
        form = FeedbackForm(instance=feedback)
        return render (request, 'vendas/modificarvendas.html',{'form':form})
    def post(self,request,id, *args, **kwargs):
        feedback = get_object_or_404(Feedback, id=id)
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('Feedback')
        else:
            return render (request, 'feedback/adicionarfeedback.html',{'form':form})
    
class ExcluirFeedbackView(View):
    def get(self,request,id, *args, **kwargs):
        feedback =Feedback.objects.get(id=id)
        feedback.delete()
        return redirect('Feedback')
                
#Vendas################################################################################################################                

class VendasView(View):
    def get(self, request, *args, **kwargs):
        vendas = Venda.objects.filter(usuario=request.user)  # Filtrar vendas pelo usuário autenticado
        return render(request, 'vendas/vendas.html', {'vendas': vendas})

class AdicionarVendasView(View):
    def get(self, request, *args, **kwargs):
        form = VendaForm()
        return render(request, 'vendas/adicionarvendas.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = VendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Vendas')
        else:
            return render(request, 'vendas/adicionarvendas.html', {'form': form})

class ModificarVendasView(View):
    def get(self, request, id, *args, **kwargs):
        venda = get_object_or_404(Venda, id=id)
        form = VendaForm(instance=venda)
        return render(request, 'vendas/modificarvendas.html', {'form': form})
    
    def post(self, request, id, *args, **kwargs):
        venda = get_object_or_404(Venda, id=id)
        form = VendaForm(request.POST, instance=venda)
        if form.is_valid():
            form.save()
            return redirect('Vendas')
        else:
            return render(request, 'vendas/modificarvendas.html', {'form': form})

class ExcluirVendasView(View):
    def get(self, request, id, *args, **kwargs):
        venda = get_object_or_404(Venda, id=id)
        venda.delete()
        return redirect('vendas')
    
def exibir_vendas(request):
    vendas = Venda.objects.filter(usuario=request.user)
    return render(request, 'vendas/vendas.html', {'vendas': vendas})

#Fornecedor################################################################################################################
class FornecedorView(View):
    def get(self,request, *args, **kwargs):
        fornecedores = Fornecedor.objects.all()
        return render (request, 'fornecedor/fornecedor.html',{'fornecedores':fornecedores})
          
class AdicionarFornecedorView(View): 
    def get(self,request, *args, **kwargs):
        form = FornecedorForm()
        return render (request, 'fornecedor/adicionarfornecedor.html',{'form':form})
    def post(self,request, *args, **kwargs):
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Fornecedor')
        else:
            return render (request, 'fornecedor/adicionarfornecedor.html',{'form':form})


class ModificarFornecedorView(View):
    def get(self,request,id, *args, **kwargs):
        fornecedor = get_object_or_404(Fornecedor, id=id)
        form = FornecedorForm(instance=fornecedor)
        return render (request, 'fornecedor/modificarfornecedor.html',{'form':form})
    def post(self,request,id, *args, **kwargs):
        fornecedor = get_object_or_404(Fornecedor, id=id)
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('Fornecedor')
        else:
            return render (request, 'fornecedor/adicionarfornecedor.html',{'form':form})
    
    
class ExcluirFornecedorView(View):
    def get(self,request,id, *args, **kwargs):
        fornecedor =Fornecedor.objects.get(id=id)
        fornecedor.delete()
        return redirect('Fornecedor')    

#Produto################################################################################################################

class ProdutosView(View):
    def get(self, request, *args, **kwargs):
        produtos = Produto.objects.all()
        user = request.user if request.user.is_authenticated else None
        return render(request, 'produtos/Produtos.html', {
            'produtos': produtos,
            'user': user
        })

    
class AdicionarProdutoView(View): 
    def get(self, request, *args, **kwargs):
        form = ProdutoForm()
        return render(request, 'produtos/adicionarproduto.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Produto')
        return render(request, 'produtos/adicionarproduto.html', {'form': form})

class ModificarProdutoView(View):
    def get(self, request, id, *args, **kwargs):
        produto = get_object_or_404(Produto, id=id)
        form = ProdutoForm(instance=produto)
        return render(request, 'produtos/modificarproduto.html', {'form': form})
    
    def post(self, request, id, *args, **kwargs):
        produto = get_object_or_404(Produto, id=id)
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('Produto')
        return render(request, 'produtos/modificarproduto.html', {'form': form})

class ExcluirProdutoView(View):
    def get(self, request, id, *args, **kwargs):
        produto = Produto.objects.get(id=id)
        produto.delete()
        return redirect('Produto')


def imagemproduto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Produto')
        else:
            return render(request, 'produto.html', {'form': form})
    else:
        form = ProdutoForm()
    return render(request, 'produtos.html', {'form': form})

def pesquisa_produtos(request):
    query = request.GET.get('q')
    produtos = Produto.objects.filter(nome__icontains=query) if query else None
    return render(request, 'produtos/pesquisa_produtos.html', {'produtos': produtos})


#Carrinho################################################################################################################
def carrinho(request):
    # Supondo que há apenas um carrinho para o exemplo
    if not Carrinho.objects.filter(usuario=request.user):
        carrinho = Carrinho.objects.create(usuario=request.user)
    carrinho = Carrinho.objects.get(usuario=request.user)
    itens = ItemCarrinho.objects.filter(carrinho=carrinho)
    total = sum(item.total_preco() for item in itens)
    return render(request, 'carrinho/ver_carrinho.html', {'carrinho': carrinho, 'itens': itens, 'total': total})

def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        form = AdicionarItemCarrinhoForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            # Supondo que há apenas um carrinho para o exemplo
            carrinho = Carrinho.objects.get(usuario=request.user)
            item.carrinho = carrinho
            item.save()
            return redirect('ver_carrinho')
    else:
        form = AdicionarItemCarrinhoForm()
    return render(request, 'carrinho/adicionar_ao_carrinho.html', {'form': form})

def remover_do_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    item.delete()
    return redirect('ver_carrinho')

from decimal import Decimal


def finalizar_compra(request):
    if request.method == 'POST':
        carrinho, criado = Carrinho.objects.get_or_create(usuario=request.user)
    
        # Buscar os itens do carrinho
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        
        # Verificar se o carrinho está vazio
        if not itens_carrinho.exists():
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('ver_carrinho')

        vendas = []  # Para armazenar as vendas criadas
        for item in itens_carrinho:
            produto = item.produto

            # Obter o estoque do produto
            try:
                estoque_produto = Estoque.objects.get(produto=produto)
            except Estoque.DoesNotExist:
                messages.error(request, f'Não há estoque suficiente para o produto {produto.nome}.')
                return redirect('ver_carrinho')

            # Verificar se o estoque é suficiente para a quantidade solicitada
            if estoque_produto.quantidade < item.quantidade:
                messages.error(request, f'Não há estoque suficiente para o produto {produto.nome}.')
                return redirect('ver_carrinho')

            # Criar a venda
            venda = Venda.objects.create(
                nome=request.user.username,
                tipovenda=item,  # Usar a instância de ItemCarrinho
                valor=produto.preco,
                quantidade=item.quantidade,
                pagamento=Decimal(produto.preco) * item.quantidade,  # Supondo pagamento imediato e exato
                datavenda=timezone.now().date(),
                usuario=request.user,
                produto=produto
            )

            categoria_dict = {
                'Frutas': 1,
                'Legumes': 2,
                'Verduras': 3,
                'Frutas e Legumes': 4,
                'Frutas e Verduras': 5,
                'Verduras e Legumes': 6,
            }

            ItensdeVenda.objects.create(
                produto=produto,
                preco=produto.preco,
                quantidade=item.quantidade,
                categoria=categoria_dict.get(produto.tipo),  # Mapeia a string para o número
                disponibilidade_estoque=estoque_produto.quantidade,
                idvendas=venda
            )

            # Atualizar o estoque após a venda
            estoque_produto.quantidade -= item.quantidade
            estoque_produto.save()

            vendas.append(venda)

        # Limpar o carrinho após finalizar a compra (remover itens do carrinho)
        itens_carrinho.delete()

        # Mostrar uma mensagem de sucesso
        messages.success(request, 'Compra finalizada com sucesso!')
        return redirect('vendas')

    return render(request, 'carrinho/finalizar_compra.html')
    if request.method == 'POST':
        carrinho, criado = Carrinho.objects.get_or_create(usuario=request.user)
    
        # Buscar os itens do carrinho
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        
        # Verificar se o carrinho está vazio
        if not itens_carrinho.exists():
            messages.error(request, 'Seu carrinho está vazio.')
            return redirect('ver_carrinho')

        vendas = []  # Para armazenar as vendas criadas
        for item in itens_carrinho:
            produto = item.produto

            # Obter o estoque do produto
            try:
                estoque_produto = Estoque.objects.get(produto=produto)
            except Estoque.DoesNotExist:
                messages.error(request, f'Não há estoque suficiente para o produto {produto.nome}.')
                return redirect('ver_carrinho')

            # Verificar se o estoque é suficiente para a quantidade solicitada
            if estoque_produto.quantidade < item.quantidade:
                messages.error(request, f'Não há estoque suficiente para o produto {produto.nome}.')
                return redirect('ver_carrinho')

            # Criar a venda
            venda = Venda.objects.create(
                nome=request.user.username,
                tipovenda=item,  # Usar a instância de ItemCarrinho
                valor=produto.preco,
                quantidade=item.quantidade,
                pagamento=Decimal(produto.preco) * item.quantidade,  # Supondo pagamento imediato e exato
                datavenda=timezone.now().date(),
                usuario=request.user,
                produto=produto
            )

            categoria_dict = {
                'Frutas': 1,
                'Legumes': 2,
                'Verduras': 3,
                'Frutas e Legumes': 4,
                'Frutas e Verduras': 5,
                'Verduras e Legumes': 6,
            }

            ItensdeVenda.objects.create(
                produto=produto,
                preco=produto.preco,
                quantidade=item.quantidade,
                categoria=categoria_dict.get(produto.tipo),  # Mapeia a string para o número
                disponibilidade_estoque=estoque_produto.quantidade,
                idvendas=venda
            )

            # Atualizar o estoque após a venda
            estoque_produto.quantidade -= item.quantidade
            estoque_produto.save()

            vendas.append(venda)

        # Limpar o carrinho após finalizar a compra (remover itens do carrinho)
        itens_carrinho.delete()

        # Mostrar uma mensagem de sucesso
        messages.success(request, 'Compra finalizada com sucesso!')
        return redirect('vendas')

    return render(request, 'carrinho/finalizar_compra.html')



#Itens de Vendas ################################################################################################################
# class ItensdeVendaView(View):
#     def get(self,request, *args, **kwargs):
#         itensdeVenda = ItensdeVenda.objects.all()
#         return render (request, 'itensvenda/itensdevenda.html',{'itensdeVenda':itensdeVenda})
    
# class AdicionarItensdeVendaView(View): 
#     def get(self,request, *args, **kwargs):
#         form = ItensdeVendaForm()
#         return render (request, 'itensvenda/adicionaritensdevenda.html',{'form':form})
#     def post(self,request, *args, **kwargs):
#         form = ItensdeVendaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('ItensdeVendas')
#         else:
#             return render (request, 'itensdevenda/adicionaritensdevenda.html',{'form':form})

# class ModificarItensdeVendaView(View):
#     def get(self,request,id, *args, **kwargs):
#         itensdevenda = get_object_or_404(Produto, id=id)
#         form = ItensdeVendaForm(instance=itensdevenda)
#         return render (request, 'itensvenda/modificaritensdevenda.html',{'form':form})
#     def post(self,request,id, *args, **kwargs):
#         itensdevenda = get_object_or_404(Produto, id=id)
#         form = ItensdeVendaForm(request.POST, instance=itensdevenda)
#         if form.is_valid():
#             form.save()
#             return redirect('Itens de Venda')
#         else:
#             return render (request, 'itensvenda/adicionaritensdevenda.html',{'form':form})
    
# class ExcluirItensdeVendaView(View):
#     def get(self,request,id, *args, **kwargs):
#         itensdevenda = ItensdeVenda.objects.get(id=id)
#         itensdevenda.delete()
#         return redirect('Itens de Venda')
    
#Estoque################################################################################################################
class EstoqueView(View):
    def get(self, request, *args, **kwargs):
        estoques = Estoque.objects.all()
        return render(request, 'estoque/estoque.html', {'estoques': estoques})


class AdicionarEstoqueView(View):
    def get(self, request, *args, **kwargs):
        form = EstoqueForm()
        return render(request, 'estoque/adicionarestoque.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = EstoqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Estoque')
        else:
            return render(request, 'estoque/adicionarestoque.html', {'form': form})


class ModificarEstoqueView(View):
    def get(self, request, id, *args, **kwargs):
        estoque = get_object_or_404(Estoque, id=id)
        form = EstoqueForm(instance=estoque)
        return render(request, 'estoque/modificarestoque.html', {'form': form})
    
    def post(self, request, id, *args, **kwargs):
        estoque = get_object_or_404(Estoque, id=id)
        form = EstoqueForm(request.POST, instance=estoque)
        if form.is_valid():
            form.save()
            return redirect('Estoque')
        else:
            return render(request, 'estoque/modificarestoque.html', {'form': form})


class ExcluirEstoqueView(View):
    def get(self, request, id, *args, **kwargs):
        estoque = get_object_or_404(Estoque, id=id)
        estoque.delete()
        return redirect('Estoque')