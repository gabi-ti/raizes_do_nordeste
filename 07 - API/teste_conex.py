from conexao import conectar_banco

try:
    conexao = conectar_banco()
    print("Conexão com o banco realizada com sucesso!")
    conexao.close()

except Exception as erro:
    print("Erro ao conectar:")
    print(erro)