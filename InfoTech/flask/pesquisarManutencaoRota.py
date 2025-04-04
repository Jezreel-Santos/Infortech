
from flask import render_template, request, flash
import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'infotech.db')
    try:
        if not os.path.exists(db_path):
            raise sqlite3.OperationalError(f"Arquivo do banco não encontrado em: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"ERRO [pesqManutRota]: Falha ao conectar ao banco: {e}")
        flash(f"Erro ao conectar ao banco ({e})", "error")
        return None

def pesquisar_manutencao():
    resultados = []
    search_criteria = {}

    if request.method == 'POST':
        tipo_pesquisa = request.form.get('tipo_pesquisa', '').strip()
        termo_pesquisa = request.form.get('termo_pesquisa', '').strip()
        search_criteria = {'tipo_pesquisa': tipo_pesquisa, 'termo_pesquisa': termo_pesquisa}
        print(f"DEBUG [pesqManutRota]: Pesquisando com tipo='{tipo_pesquisa}', termo='{termo_pesquisa}'")

        # ... (validações como antes) ...
        if not tipo_pesquisa:
            flash("Selecione um tipo de pesquisa.", "warning")
            # Retorna aqui para exibir o flash imediatamente
            return render_template('pesquisar-manutencao.html', resultados=resultados, search_criteria=search_criteria)
        tipos_com_id = ['codigo_manutencao', 'codigo_cliente']
        if tipo_pesquisa in tipos_com_id:
            if not termo_pesquisa:
                flash("Informe o ID para pesquisar.", "warning")
                return render_template('pesquisar-manutencao.html', resultados=resultados, search_criteria=search_criteria)
            if not termo_pesquisa.isdigit():
                flash("O ID deve ser um número.", "error")
                return render_template('pesquisar-manutencao.html', resultados=resultados, search_criteria=search_criteria)
        tipos_status = ['orcamento', 'emManutencao', 'aguardandoPeca', 'pronto', 'naoAprovado', 'entregue']

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                base_query = """
                    SELECT m.*, c.nome as nome_cliente FROM manutencao m
                    LEFT JOIN clientes c ON m.codigo_cliente = c.id_cliente WHERE """
                params = []

                if tipo_pesquisa == 'codigo_manutencao':
                    base_query += "m.codigo_manutencao = ?"
                    params.append(int(termo_pesquisa))
                elif tipo_pesquisa == 'codigo_cliente':
                    base_query += "m.codigo_cliente = ?"
                    params.append(int(termo_pesquisa))
                elif tipo_pesquisa in tipos_status:
                    base_query += "m.status_manutencao = ?"
                    params.append(tipo_pesquisa)
                else:
                    flash("Tipo de pesquisa desconhecido.", "error")
                    base_query = None

                if base_query:
                    base_query += " ORDER BY m.codigo_manutencao DESC"
                    print(f"DEBUG [pesqManutRota]: Executando: {base_query} com {params}")
                    cursor.execute(base_query, params)
                    resultados = cursor.fetchall() # Pega os resultados
                    if not resultados:
                        flash("Nenhuma manutenção encontrada.", "info")
                    else:
                         flash(f"{len(resultados)} manutenção(ões) encontrada(s).", "success")

            except sqlite3.Error as e:
                print(f"ERRO DB [pesqManutRota]: {e}")
                flash(f"Erro ao consultar o banco: {e}", "error")
                resultados = [] # Garante que resultados esteja vazio em caso de erro
            # ... (outros excepts como antes) ...
            finally:
                if conn: conn.close()
        # else: flash já foi emitido

        # <<< ADICIONAR ESTE PRINT DE DEPURAÇÃO >>>
        print("-" * 30)
        print(f"DEBUG [pesqManutRota]: Enviando para o template:")
        print(f" -> Quantidade de Resultados: {len(resultados)}")
        # Mostra o primeiro resultado (se houver) para verificar a estrutura
        if resultados:
            try:
                # Tenta converter a primeira linha (sqlite3.Row) para dict para exibição
                print(f" -> Primeiro Resultado: {dict(resultados[0])}")
            except Exception as print_err:
                print(f" -> Primeiro Resultado (erro ao converter p/ dict): {resultados[0]} - Erro: {print_err}")
        else:
             print(" -> Primeiro Resultado: Nenhum")
        print(f" -> Critérios: {search_criteria}")
        print("-" * 30)
        # <<< FIM DO PRINT DE DEPURAÇÃO >>>

        return render_template('pesquisar-manutencao.html', resultados=resultados, search_criteria=search_criteria)

    # Método GET
    return render_template('pesquisar-manutencao.html', resultados=resultados, search_criteria=search_criteria)