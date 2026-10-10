import pyodbc

def conectar_banco():
    conexao = pyodbc.connect(
        #IDENTIFICAÇÃO DA VERSÃO SO DRIVER DO ODBC IDENTIFICADO NO COMPUTADOR#
        "DRIVER={ODBC Driver 17 for SQL Server};" 
        #O SERVIDOR/INSTÂNCIA DO SQL SERVER#
        "SERVER=DESKTOP-E8G0FNV\\SQLExpress;"
        #O BANCO PRINCIPAL#
        "DATABASE=RaizesNordeste;"
        #USA A AUTENTICAÇÃO DO WINDOWS#
        "Trusted_Connection=yes;"
        #PERMITE A CONEXÃO LOCAL COM O CERTIFICADO DO SERVIDOR.#
        "TrustServerCertificate=yes;"
    )

    return conexao
    