from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    endereco = models.CharField(max_length=100, verbose_name="Endereço do usuário")
    telefone = models.CharField(max_length=20, verbose_name="Telefone do usuário")
    cidade = models.CharField(max_length=65, verbose_name="Cidade do usuário")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"



class Feedback(models.Model):
    comentarios = models.CharField(max_length=100, verbose_name="Texto do comentário")
    avaliacoes = models.IntegerField(choices=[
        (1, 'Muito Ruim'),
        (2, 'Ruim'),
        (3, 'Regular'),
        (4, 'Bom'),
        (5, 'Muito Bom')
    ], verbose_name="Avaliação do feedback")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")

    def __str__(self):
        return f"{self.usuario.username}, {self.comentarios}, {self.get_avaliacoes_display()}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Fornecedor")
    CPF = models.CharField(max_length=50, unique=True, verbose_name="CPF do Fornecedor")
    email = models.EmailField(max_length=100, verbose_name="Email do Fornecedor")  
    endereco = models.CharField(max_length=100, verbose_name="Endereço do Fornecedor")
    telefone = models.CharField(max_length=20, verbose_name="Telefone do Fornecedor")
    cidade = models.CharField(max_length=65, verbose_name="Cidade do Fornecedor")
    def __str__(self):
        return f"{self.nome},{self.CPF},{self.email},{self.endereco},{self.telefone},{self.cidade}"
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

class Produto(models.Model):
    TIPOS = [
        ('Frutas', 'Frutas'),
        ('Verduras', 'Verduras'),
        ('Legumes', 'Legumes'),
    ]
    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    tipo = models.CharField(choices=TIPOS, max_length=20, verbose_name="Tipo de Produto")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Produto")
    quantidade = models.CharField(max_length=100, verbose_name="Quantidade de Produto")
    imagem = models.ImageField(upload_to='static/imgs', null=True, blank=True, verbose_name="Imagem")
    idfornecedor = models.ForeignKey('Fornecedor', on_delete=models.CASCADE, verbose_name="Fornecedor")

    def __str__(self):
        return f"{self.nome}, {self.get_tipo_display()}, {self.preco}, {self.quantidade}, {self.imagem}, {self.idfornecedor}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"




class Estoque(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, verbose_name="Produto",null=True,related_name="estoque")
    quantidade = models.IntegerField(verbose_name="Quantidade de Produto")

    def __str__(self):
        return f"Produto: {self.produto.nome}, Quantidade: {self.quantidade}"

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

class Carrinho(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def total_preco(self):
        return self.quantidade * self.produto.preco
class Venda(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Usuário")
    tipovenda = models.ForeignKey('ItemCarrinho', on_delete=models.CASCADE, verbose_name="Tipo de Venda")  # Remover max_length aqui
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    pagamento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Pagamento")
    datavenda = models.DateField(verbose_name="Data da Venda")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário", null=True, blank=True)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, verbose_name="Produto", null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.produto:
            # Validar a existência de estoque
            estoque_item = Estoque.objects.filter(produto=self.produto).first()
            if not estoque_item:
                raise ValueError(f"O produto '{self.produto.nome}' não possui registro no estoque.")
            
            # Validar a quantidade disponível no estoque
            if estoque_item.quantidade < self.quantidade:
                raise ValueError(f"Quantidade insuficiente no estoque para o produto '{self.produto.nome}'.")

            # Atualizar o estoque antes de salvar a venda
            estoque_item.quantidade -= self.quantidade
            estoque_item.save()

        # Salvar a venda
        super(Venda, self).save(*args, **kwargs)

    def __str__(self):
        return f"Usuário: {self.usuario.username}, Tipo de Venda: {self.tipovenda}, Valor: {self.valor}, Quantidade: {self.quantidade}, Pagamento: {self.pagamento}, Data: {self.datavenda}, Produto: {self.produto.nome}"

    @property
    def total(self):
        return self.valor * self.quantidade

    @property
    def troco(self):
        if self.pagamento >= self.total:
            return self.pagamento - self.total
        else:
            return 0

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"



class ItensdeVenda(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Nome do Produto", null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor do Produto")
    quantidade = models.IntegerField(verbose_name="Quantidade do Produto")
    categoria = models.IntegerField(choices=[
        (1, 'Frutas'),
        (2, 'Legumes'),
        (3, 'Verduras'),
        (4, 'Frutas e Legumes'),
        (5, 'Frutas e Verduras'),
        (6, 'Verduras e Legumes')
    ], verbose_name="Categoria do Produto")
    disponibilidade_estoque = models.CharField(null=True,max_length=100, verbose_name="Produto Disponíveis no Estoque")
    idvendas = models.ForeignKey(Venda, on_delete=models.CASCADE, verbose_name="Vendas")

    def __str__(self):
        return f"Produto: {self.produto.nome}, Preço: {self.preco}, Quantidade: {self.quantidade}, Categoria: {self.get_categoria_display()}, Disponibilidade no Estoque: {self.disponibilidade_estoque}, Venda: {self.idvendas}"

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"
