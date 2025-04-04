function estadoMenu(menuItem) {
    const subMenu = menuItem.querySelector('ul');
    if (!subMenu) return;

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

    if (subMenu.style.display === "block") {
        subMenu.style.display = "none";
        menuItem.classList.remove('active');
    } else {
        subMenu.style.display = "block";
        menuItem.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const buscarClienteButton = document.getElementById('buscar_cliente');
    const buscaSection = document.getElementById('busca_cliente_section'); 
    const infoClienteDiv = document.getElementById('info_cliente'); 
    const form = infoClienteDiv.querySelector('form'); 
    const mensagemErroDiv = document.getElementById('mensagem_erro');

    // Inputs do formulário
    const idClienteInputBusca = document.getElementById('cliente_id_busca'); 
    const idClienteInputForm = document.getElementById('id_cliente_form'); 
    const nomeInput = document.getElementById('anome');
    const cpfInput = document.getElementById('acpf');
    const telefoneInput = document.getElementById('atelCliente');
    const emailInput = document.getElementById('aemailCliente');
    const enderecoInput = document.getElementById('aenderecoCliente');

    let originalData = {}; 

    buscarClienteButton.addEventListener('click', () => {
        const clienteId = idClienteInputBusca.value;

        // Limpa erros e esconde form
        mensagemErroDiv.style.display = 'none';
        mensagemErroDiv.textContent = '';
        infoClienteDiv.style.display = 'none';

        if (!clienteId || isNaN(clienteId)) {
            mensagemErroDiv.style.display = 'block';
            mensagemErroDiv.textContent = 'Por favor, insira um ID de cliente válido.';
            idClienteInputBusca.focus();
            return;
        }

        fetch(`/buscar_cliente/${clienteId}`)
            .then(response => {
                 if (response.status === 404) {
                    return null; // Não encontrado
                }
                if (!response.ok) {
                     return response.json().then(errData => {
                         throw new Error(errData.erro || `Erro na requisição: ${response.status}`);
                    }).catch(() => {
                         throw new Error(`Erro na requisição: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    // Preenche o formulário
                    idClienteInputForm.value = data.id_cliente || ''; // ID no campo oculto
                    nomeInput.value = data.nome || '';
                    cpfInput.value = data.cpf || '';
                    telefoneInput.value = data.telefone || '';
                    emailInput.value = data.email || '';
                    enderecoInput.value = data.endereco || '';

                    // Armazena os dados originais
                    originalData = {
                        nome: data.nome || '',
                        cpf: data.cpf || '',
                        telefone: data.telefone || '',
                        email: data.email || '',
                        endereco: data.endereco || ''
                    };

                    // Mostra o formulário e esconde a busca
                    infoClienteDiv.style.display = 'flex'; 
                    // buscaSection.style.display = 'none'; 
                    mensagemErroDiv.style.display = 'none';

                } else {
                    mensagemErroDiv.style.display = 'block';
                    mensagemErroDiv.textContent = 'Cliente não encontrado.';
                    infoClienteDiv.style.display = 'none'; 
                    idClienteInputBusca.focus();
                }
            })
            .catch(error => {
                console.error("Erro ao buscar cliente:", error);
                mensagemErroDiv.style.display = 'block';
                mensagemErroDiv.textContent = `Erro: ${error.message}`;
                infoClienteDiv.style.display = 'none';
            });
    });

    // Evento de submit do formulário
    form.addEventListener('submit', (event) => {
        // Verifica se houve alterações
        const currentData = {
            nome: nomeInput.value,
            cpf: cpfInput.value,
            telefone: telefoneInput.value,
            email: emailInput.value,
            endereco: enderecoInput.value
        };

        let hasChanged = false;
        for (const key in currentData) {
            if (currentData[key] !== originalData[key]) {
                hasChanged = true;
                break;
            }
        }

        if (!hasChanged) {
            event.preventDefault(); // Impede o envio do formulário
            mensagemErroDiv.textContent = 'Nenhuma alteração detectada para salvar.';
            mensagemErroDiv.style.display = 'block';
            alert('Nenhuma alteração detectada.');
        } else {
             mensagemErroDiv.style.display = 'none'; 
        }
    });
});

