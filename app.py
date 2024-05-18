from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados SQLite
DATABASE = 'database.db'

@app.route("/")
def home():
    return render_template("home.html")

# Função para criar as tabelas no banco de dados
def create_tables():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Tabela Clientes
        cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                        CNPJ TEXT PRIMARY KEY,
                        Primeiro_Nome TEXT,
                        Segundo_Nome TEXT,
                        Email TEXT,
                        Telefone TEXT,
                        Estado TEXT,
                        Cidade TEXT,
                        Bairro TEXT,
                        Rua TEXT,
                        Numero TEXT)''')
        # Tabela Obras
        cursor.execute('''CREATE TABLE IF NOT EXISTS Obras (
                        OS TEXT PRIMARY KEY,
                        Primeiro_Nome_Contato TEXT,
                        Segundo_Nome_Contato TEXT,
                        Valor REAL,
                        Estado_Obra TEXT,
                        Cidade_Obra TEXT,
                        Bairro_Obra TEXT,
                        Rua_Obra TEXT,
                        Numero_Obra TEXT,
                        CNPJ_Cliente TEXT,
                        FOREIGN KEY (CNPJ_Cliente) REFERENCES Clientes(CNPJ))''')
        # Tabela Compras
        cursor.execute('''CREATE TABLE IF NOT EXISTS Compras (
                        Obra_OS TEXT,
                        Ordem_de_Compras TEXT PRIMARY KEY,
                        Materia_prima TEXT,
                        Consumiveis TEXT,
                        Miscelanea TEXT,
                        FOREIGN KEY (Obra_OS) REFERENCES Obras(OS))''')
        conn.commit()


# Rota para a página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Cadastro de Cliente
        cnpj = request.form['cnpj']
        primeiro_nome = request.form['primeiro_nome']
        segundo_nome = request.form['segundo_nome']
        email = request.form['email']
        telefone = request.form['telefone']
        estado = request.form['estado']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        rua = request.form['rua']
        numero = request.form['numero']

        # Cadastro de Obra
        os = request.form['os']
        primeiro_nome_contato = request.form['primeiro_nome_contato']
        segundo_nome_contato = request.form['segundo_nome_contato']
        valor = request.form['valor']
        estado_obra = request.form['estado_obra']
        cidade_obra = request.form['cidade_obra']
        bairro_obra = request.form['bairro_obra']
        rua_obra = request.form['rua_obra']
        numero_obra = request.form['numero_obra']

        # Cadastro de Compra
        ordem_compra = request.form['ordem_compra']
        materia_prima = request.form['materia_prima']
        consumiveis = request.form['consumiveis']
        miscelanea = request.form['miscelanea']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Cadastro de Cliente
            cursor.execute('''INSERT INTO Clientes (CNPJ, Primeiro_Nome, Segundo_Nome, Email, Telefone, Estado, Cidade, Bairro, Rua, Numero)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (cnpj, primeiro_nome, segundo_nome, email, telefone, estado, cidade, bairro, rua, numero))
            # Cadastro de Obra
            cursor.execute('''INSERT INTO Obras (OS, Primeiro_Nome_Contato, Segundo_Nome_Contato, Valor, Estado_Obra, Cidade_Obra, Bairro_Obra, Rua_Obra, Numero_Obra, CNPJ_Cliente)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            os, primeiro_nome_contato, segundo_nome_contato, valor, estado_obra, cidade_obra, bairro_obra, rua_obra,
            numero_obra, cnpj))
            # Cadastro de Compra
            cursor.execute('''INSERT INTO Compras (Obra_OS, Ordem_de_Compras, Materia_prima, Consumiveis, Miscelanea)
                              VALUES (?, ?, ?, ?, ?)''', (os, ordem_compra, materia_prima, consumiveis, miscelanea))
            conn.commit()
        return redirect(url_for('cadastro'))
    return render_template('cadastro.html')


# Rota para a página de consulta
@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        cnpj = request.form['cnpj']
        os = request.form['os']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM Obras WHERE CNPJ_Cliente = ?''', (cnpj,))
            obras = cursor.fetchall()
            cursor.execute('''SELECT * FROM Clientes WHERE CNPJ = ?''', (cnpj,))
            cliente = cursor.fetchone()
            if cliente:
                if os:
                    cursor.execute('''SELECT * FROM Compras WHERE Obra_OS = ?''', (os,))
                    compras = cursor.fetchall()
                    return render_template('consulta.html', cliente=cliente, obras=obras, compras=compras)
                else:
                    return render_template('consulta.html', cliente=cliente, obras=obras)
            else:
                return render_template('consulta.html', mensagem='Cliente não encontrado')
    return render_template('consulta.html')

# Função para limpar todas as tabelas do banco de dados
def limpar_banco():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM Compras''')
        cursor.execute('''DELETE FROM Obras''')
        cursor.execute('''DELETE FROM Clientes''')
        conn.commit()

# Rota para limpar o banco de dados
@app.route('/limpar_banco')
def limpar():
    limpar_banco()
    return 'Banco de dados limpo com sucesso.'

if __name__ == '__main__':
    create_tables()  # Criar tabelas ao iniciar a aplicação
    app.run(debug=True)

