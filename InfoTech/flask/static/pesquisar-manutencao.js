
function estadoMenu(menuItem) {
    const subMenu = menuItem.querySelector('ul');
    if (!subMenu) { console.warn("Submenu não encontrado para o item:", menuItem); return; }
    const parentUl = menuItem.parentElement;
    if (parentUl) {
        const siblingLis = parentUl.querySelectorAll(':scope > li');
        siblingLis.forEach(li => {
            if (li !== menuItem) {
                const otherSubMenu = li.querySelector('ul');
                if (otherSubMenu) { otherSubMenu.style.display = "none"; li.classList.remove('active'); }
            }
        });
    } else { console.warn("Elemento pai <ul> não encontrado para:", menuItem); }
    if (subMenu.style.display === "block") { subMenu.style.display = "none"; menuItem.classList.remove('active'); }
    else { subMenu.style.display = "block"; menuItem.classList.add('active'); }
}

/*
  Controla a visibilidade e o estado 'required' do campo de texto (ID)
  baseado no tipo de pesquisa selecionado (ID ou Status).
 */
function toggleTermoPesquisaField() {
    const tipoPesquisaHiddenInput = document.getElementById('tipo_pesquisa_hidden');
    const termoPesquisaContainer = document.getElementById('termo_pesquisa_container');
    const termoPesquisaInput = document.getElementById('termo_pesquisa_input');

    if (!tipoPesquisaHiddenInput || !termoPesquisaContainer || !termoPesquisaInput) {
        console.error("Elementos do formulário de pesquisa não encontrados para toggle.");
        return;
    }

    const tipoSelecionado = tipoPesquisaHiddenInput.value;

    // --- Lista Padronizada de Status (que NÃO usam o campo de ID) ---
    const statusList = ['orcamento', 'emManutencao', 'aguardandoPeca', 'pronto', 'naoAprovado', 'entregue'];


    // --- Fim da Lista ---

    // Verifica se o tipo selecionado requer o campo de termo (ID)
    if (tipoSelecionado === 'codigo_manutencao' || tipoSelecionado === 'codigo_cliente') {
        termoPesquisaContainer.style.display = 'flex'; // Mostra o container do input de ID
        termoPesquisaInput.required = true; 
        termoPesquisaInput.placeholder = tipoSelecionado === 'codigo_manutencao' ? 'Digite o ID da Manutenção' : 'Digite o ID do Cliente';
    }
    // Verifica se é um dos status da lista
    else if (statusList.includes(tipoSelecionado)) {
        termoPesquisaContainer.style.display = 'none'; // Esconde o container do input de ID
        termoPesquisaInput.required = false;
        termoPesquisaInput.value = ''; // Limpa o valor
    }
    // Caso padrão (nenhum tipo selecionado ou tipo inválido)
    else {
         termoPesquisaContainer.style.display = 'none';
         termoPesquisaInput.required = false;
         termoPesquisaInput.value = '';
    }
}


// Lógica principal da página
document.addEventListener('DOMContentLoaded', () => {

    // --- Lógica para o Custom Select ---
    const selectContainer = document.getElementById('tipoPesquisaContainer');
    if (selectContainer) {
        const selectedDisplay = selectContainer.querySelector('.selected');
        const optionsContainer = selectContainer.querySelector('.options');
        const optionList = selectContainer.querySelectorAll('.option');
        const hiddenInput = document.getElementById('tipo_pesquisa_hidden');

        if (selectedDisplay && optionsContainer && optionList.length > 0 && hiddenInput) {
            // Placeholder inicial
            if (!hiddenInput.value) { selectedDisplay.setAttribute('data-placeholder', 'true'); }
            else { selectedDisplay.removeAttribute('data-placeholder'); } // Garante remoção se houver valor inicial

            // Abrir/Fechar
            selectedDisplay.addEventListener('click', (event) => {
                event.stopPropagation();
                const isActive = selectContainer.classList.contains('active');
                document.querySelectorAll('.custom-select.active').forEach(activeSelect => {
                    if (activeSelect !== selectContainer) {
                         activeSelect.classList.remove('active');
                         activeSelect.querySelector('.options').style.display = 'none';
                    }
                });
                selectContainer.classList.toggle('active');
                optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
            });

            // Selecionar opção
            optionList.forEach(option => {
                option.addEventListener('click', () => {
                    selectedDisplay.textContent = option.textContent;
                    const newValue = option.dataset.value;
                    hiddenInput.value = newValue;
                    selectedDisplay.removeAttribute('data-placeholder');
                    optionsContainer.style.display = 'none';
                    selectContainer.classList.remove('active');

                    //CHAMA A FUNÇÃO PARA MOSTRAR/ESCONDER O CAMPO DE TEXTO
                    toggleTermoPesquisaField();

                    hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
                });
            });
        } else {
             console.warn("Estrutura do custom select 'tipoPesquisaContainer' inválida.");
        }
    } else {
         console.warn("Elemento 'tipoPesquisaContainer' não encontrado.");
    }

    // Fechar selects ao clicar fora
    document.addEventListener('click', (event) => {
        document.querySelectorAll('.custom-select.active').forEach(activeSelect => {
            if (!activeSelect.contains(event.target)) {
                activeSelect.classList.remove('active');
                activeSelect.querySelector('.options').style.display = 'none';
            }
        });
    });

    toggleTermoPesquisaField();

});

