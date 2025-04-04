
from flask import flash, redirect, render_template, request, url_for, g
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'infotech.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        try:
            if not os.path.exists(DATABASE):
                 raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {DATABASE}")
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"ERRO [cadClienteRota]: {e}")
            flash(f"Erro crítico ao conectar ao banco: {e}", "error")
            return None
    return db

def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def cadastrar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        endereco = request.form.get("endereco", "").strip()

        if not all([nome, cpf, telefone, email, endereco]):
             flash("Erro: Preencha todos os campos obrigatórios.", "error")
             return redirect(url_for("cadastrar_cliente"))

        conn = get_db()
        if conn is None:
            return redirect(url_for("cadastrar_cliente"))

        try:
            # Verifica se CPF já existe ANTES de tentar inserir
            cur = conn.cursor()
            cur.execute("SELECT id_cliente FROM clientes WHERE cpf = ?", (cpf,))
            existing_client = cur.fetchone()
            if existing_client:
                flash("Erro: CPF já cadastrado.", "error")
                return redirect(url_for("cadastrar_cliente"))

            # Insere se CPF não existe
            conn.execute(
                """INSERT INTO clientes (nome, cpf, telefone, email, endereco, data_cadastro, hora_cadastro)
                   VALUES (?, ?, ?, ?, ?, DATE('now', 'localtime'), TIME('now', 'localtime'))""",
                (nome, cpf, telefone, email, endereco)
            )
            conn.commit()
            flash("Cliente cadastrado com sucesso!", "success")
            print(f"INFO [cadClienteRota]: Cliente '{nome}' (CPF: {cpf}) cadastrado.")
            return redirect(url_for("cadastrar_cliente"))

        except sqlite3.Error as e:
            conn.rollback() # Desfaz alterações em caso de erro
            print(f"ERRO [cadClienteRota]: {e}")
            flash(f"Erro ao cadastrar cliente: {e}", "error")
            return redirect(url_for("cadastrar_cliente"))

    return render_template("cadastrar-cliente.html")