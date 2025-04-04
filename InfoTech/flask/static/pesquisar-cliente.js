function estadoMenu(menuItem) {
    const subMenu = menuItem.querySelector('ul');
    if (!subMenu) return; 

    // Fecha outros submenus abertos no mesmo nível (opcional, mas bom para UX)
    const parentUl = menuItem.parentElement;
    const siblingLis = parentUl.querySelectorAll(':scope > li');
    siblingLis.forEach(li => {
        if (li !== menuItem) {
            const otherSubMenu = li.querySelector('ul');
            if (otherSubMenu) {
                otherSubMenu.style.display = "none";
                li.classList.remove('active');
            }
        }
    });

    // Alterna o submenu atual
    if (subMenu.style.display === "block") {
        subMenu.style.display = "none";
        menuItem.classList.remove('active');
    } else {
        subMenu.style.display = "block";
        menuItem.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const pesquisarClienteForm = document.getElementById('pesquisar_cliente_form');
    const formContainer = document.getElementById('pesquisa_client_princ'); // Container do formulário
    const infoClienteDiv = document.getElementById('info_cliente'); // Container da tabela
    const tabelaClienteBody = document.getElementById('cliente_table').getElementsByTagName('tbody')[0]; // Corpo da tabela
    const mensagemErroDiv = document.getElementById('mensagem_erro');

    pesquisarClienteForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Previne o envio padrão do formulário

        const clienteIdInput = document.getElementById('cliente_id');
        const clienteId = clienteIdInput.value;

        // Limpa mensagens de erro e tabela anteriores
        mensagemErroDiv.style.display = 'none';
        mensagemErroDiv.textContent = '';
        tabelaClienteBody.innerHTML = ''; // Limpa o corpo da tabela
        infoClienteDiv.style.display = 'none'; // Esconde a tabela antes da busca

        if (!clienteId || isNaN(clienteId)) {
            mensagemErroDiv.style.display = 'block';
            mensagemErroDiv.textContent = 'Favor inserir um ID de cliente válido.';
            clienteIdInput.focus();
            return;
        }

        console.log('Buscando ID do cliente:', clienteId);

        fetch(`/buscar_cliente/${clienteId}`)
            .then(response => {
                if (response.status === 404) {
                    return null; // Cliente não encontrado
                }
                if (!response.ok) {
                    // Tenta pegar uma mensagem de erro do corpo da resposta, se houver
                    return response.json().then(errData => {
                         throw new Error(errData.erro || `Erro na requisição: ${response.status}`);
                    }).catch(() => {
                         throw new Error(`Erro na requisição: ${response.status}`); 
                    });
                }
                return response.json(); // Cliente encontrado
            })
            .then(data => {
                console.log('Dados recebidos:', data);

                if (data) {
                    // Preenche a tabela
                    const row = tabelaClienteBody.insertRow();
                    row.insertCell().textContent = data.id_cliente || '';
                    row.insertCell().textContent = data.nome || '';
                    row.insertCell().textContent = data.cpf || '';
                    row.insertCell().textContent = data.telefone || '';
                    row.insertCell().textContent = data.email || '';
                    row.insertCell().textContent = data.endereco || '';
                    row.insertCell().textContent = data.data_cadastro || '';
                    row.insertCell().textContent = data.hora_cadastro || '';

                    // Esconde o formulário e mostra a tabela
                    formContainer.style.display = 'none';
                    infoClienteDiv.style.display = 'block'; // Mostra o container da tabela
                    mensagemErroDiv.style.display = 'none'; // Garante que não há erro visível

                } else {
                    // Cliente não encontrado (status 404)
                    mensagemErroDiv.textContent = 'Cliente não encontrado.';
                    mensagemErroDiv.style.display = 'block';
                    infoClienteDiv.style.display = 'none'; // Garante que a tabela não é mostrada
                    formContainer.style.display = 'block'; // Mantém o formulário visível
                    clienteIdInput.focus(); // Coloca o foco de volta no input
                }
            })
            .catch(error => {
                console.error('Erro no fetch:', error);
                mensagemErroDiv.style.display = 'block';
                mensagemErroDiv.textContent = `Erro ao buscar cliente: ${error.message}`;
                infoClienteDiv.style.display = 'none'; // Esconde a tabela
                formContainer.style.display = 'block'; // Mostra o formulário de novo
            });
    });
});


