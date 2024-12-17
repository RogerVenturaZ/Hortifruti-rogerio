from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    
    path('feedback/', FeedbackView.as_view(), name='Feedback'),
    path('adicionarfeedback/', AdicionarFeedbackView.as_view(), name='Adicionar Feedback'),
    path('modificarfeedback/<int:id>', ModificarFeedbackView.as_view(), name='Modificar Feedback'),
    path('excluirfeedback/<int:id>', ExcluirFeedbackView.as_view(), name='Excluir Feedback'),
    
    path('vendas/', VendasView.as_view(), name='vendas'), 
    path('vendas/adicionar/', AdicionarVendasView.as_view(), name='AdicionarVendas'),
    path('vendas/mificar/<int:id>/', ModificarVendasView.as_view(), name='ModificarVendas'),
    path('vendas/excluir/<int:id>/', ExcluirVendasView.as_view(), name='ExcluirVendas'),
    
    path('fornecedor/', FornecedorView.as_view(), name='Fornecedor'),
    path('adicionarfornecedor/', AdicionarFornecedorView.as_view(), name='Adicionar Fornecedor'),
    path('modificarfornecedor/<int:id>', ModificarFornecedorView.as_view(), name='Modificar Fornecedor'),
    path('excluirfornecedor/<int:id>', ExcluirFornecedorView.as_view(), name='Excluir Fornecedor'),
    
    path('produto/', ProdutosView.as_view(), name='Produto'),
    path('adicionarproduto/', AdicionarProdutoView.as_view(), name='Adicionar Produto'),
    path('modificarproduto/<int:id>', ModificarProdutoView.as_view(), name='Modificar Produto'),
    path('excluirproduto/<int:id>', ExcluirProdutoView.as_view(), name='Excluir Produto'),
    
    path('pesquisa/', pesquisa_produtos, name='pesquisa_produtos'),
    
    path('carrinho/', carrinho, name='ver_carrinho'),
    path('carrinho/adicionar/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/remover/<int:item_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    
    # path('itensdevenda/', ItensdeVendaView.as_view(), name='ItensdeVendas'),
    # path('adicionaritensdevenda/', AdicionarItensdeVendaView.as_view(), name='Adicionar Itens de Vendas'),
    # path('modificaritensdevenda/<int:id>', ModificarItensdeVendaView.as_view(), name='Modificar Itens de Vendas'),
    # path('excluiritensdevenda/<int:id>', ExcluirItensdeVendaView.as_view(), name='Excluir Itens de Vendas'),
    
    path('perfil/<int:id>/', PerfilView.as_view(), name='perfil'),
    path('adicionarperfil/', AdicionarPerfilView.as_view(), name='adicionar_perfil'),
    path('modificarperfil/<int:id>/', ModificarPerfilView.as_view(), name='modificar_perfil'),
    path('excluirperfil/<int:id>/', ExcluirPerfilView.as_view(), name='excluir_perfil'),
    
    path('login/', LoginView.as_view(), name='login'),
    
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    
    path('logout/', LogoutView.as_view(), name='Logout'),
    
    path('estoque/', EstoqueView.as_view(), name='Estoque'),
    path('adicionarestoque/', AdicionarEstoqueView.as_view(), name='Adicionar Estoque'),
    path('modificarestoque/<int:id>', ModificarEstoqueView.as_view(), name='Modificar Estoque'),
    path('excluirestoque/<int:id>', ExcluirEstoqueView.as_view(), name='Excluir Estoque'),
    path('finalizar_compra/', finalizar_compra, name='finalizar_compra'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
