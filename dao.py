#dao = Data Acess Objetct ou Objeto de Acesso a Dados
#módulo responsável pelo acesso ao banco de dados
import sqlite3
from produto import Produto

SQL_PREPARA_BANCO = 'create table if not exists produto (' \
                       'descricao varchar(60) not null,' \
                       'preco double not null,' \
                       'quantidade integer not null' \
                      ');'

SQL_SALVA_PRODUTO = 'insert into produto values (?, ?, ?)'
SQL_LISTA_PRODUTOS = 'SELECT DESCRICAO, PRECO, QUANTIDADE, ROWID FROM PRODUTO'
SQL_PRODUTO_POR_ID = 'SELECT DESCRICAO, PRECO, QUANTIDADE, ROWID FROM PRODUTO WHERE rowid=?'
SQL_ATUALIZA_PRODUTO = 'update produto set descricao=?, preco=?, quantidade=? where rowid=?'
SQL_DELETA_PRODUTO = 'delete from produto where rowid=?'

class ProdutoDao:

    def __init__(self, nome_banco):
        self.__nome_banco = nome_banco
        self.prepara_banco()

    def prepara_banco(self):
        print('Conectando com o banco de dados...', end='')
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_PREPARA_BANCO)
        #comitando senão nada terá efeito
        conexao.commit()
        print('OK')

    def salvar(self, produto):
        print('Testando ID:', produto.id)
        print('Salvando produto...', end='')
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()

        #verifica se existe um id válido
        if (produto.id != None and len(produto.id) > 0):
            cursor.execute(SQL_ATUALIZA_PRODUTO, (produto.descricao, produto.preco, produto.quantidade, produto.id))
        else:
            cursor.execute(SQL_SALVA_PRODUTO, (produto.descricao, produto.preco, produto.quantidade))
            produto.id = cursor.lastrowid

        conexao.commit()
        print('OK')
        return produto #devolve o mesmo produto, porém agora com o id

    def listar(self):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_LISTA_PRODUTOS)
        #converte a lista de dados em lista de objetos tipo Produto
        produtos = traduz_produtos(cursor.fetchall())
        #print(produtos)
        return produtos

    def deletar(self, id):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_DELETA_PRODUTO, [id])
        conexao.commit()

    def busca_por_id(self, id):
        conexao = sqlite3.connect(self.__nome_banco)
        cursor = conexao.cursor()
        cursor.execute(SQL_PRODUTO_POR_ID, [str(id)])
        return cria_produto_com_tupla(cursor.fetchone())




#lista_tuplas = [('TV LG 50"', 3999.0, 5, 1), ('TV LG 50"', 3999.0, 5, 2)]

def traduz_produtos(lista_tuplas):
    # produtos = traz em forma de tupla [('TV LG 50"', 3999.0, 5, 1), ('TV LG 50"', 3999.0, 5, 2)]
    return list(map(cria_produto_com_tupla, lista_tuplas))

#tupla = ('TV LG 50"', 3999.0, 5, 1)
def cria_produto_com_tupla(tupla):
    return Produto(tupla[0], tupla[1], tupla[2], tupla[3])


