
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


function confirmarExclusao() {
    // Pega o ID da manutenção do botão ou de um campo, se necessário para a mensagem
    const manutIdElement = document.querySelector('input[name="manutencao_id_delete"]');
    const manutId = manutIdElement ? manutIdElement.value : 'este registro';
    return confirm(`Tem certeza que deseja excluir permanentemente a manutenção ID ${manutId}? Esta ação não pode ser desfeita.`);
}


// --- Lógica para o Custom Select de Status ---
document.addEventListener('DOMContentLoaded', () => {
    // Encontra o container do select (apenas se a seção de update estiver visível)
    const selectContainer = document.getElementById('statusManutencaoContainer');

    if (selectContainer) { // Executa só se o container do select existir na página
        const selectedDisplay = selectContainer.querySelector('.selected');
        const optionsContainer = selectContainer.querySelector('.options');
        const optionList = selectContainer.querySelectorAll('.option');
        // O input hidden associado
        const hiddenInput = document.getElementById('status_manutencao_hidden');

        if (!selectedDisplay || !optionsContainer || !optionList.length || !hiddenInput) {
            console.warn("Estrutura do custom select 'statusManutencaoContainer' inválida ou incompleta.");
            return;
        }

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
            // Alterna o atual
            selectContainer.classList.toggle('active');
            optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
        });

        // Selecionar opção
        optionList.forEach(option => {
            option.addEventListener('click', () => {
                selectedDisplay.textContent = option.textContent;
                const newValue = option.dataset.value;
                hiddenInput.value = newValue; 
                optionsContainer.style.display = 'none';
                selectContainer.classList.remove('active');
                hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
            });
        });

         // Fechar selects ao clicar fora
        document.addEventListener('click', (event) => {
            if (selectContainer.classList.contains('active') && !selectContainer.contains(event.target)) {
                 selectContainer.classList.remove('active');
                 optionsContainer.style.display = 'none';
             }
        });

    } 
});

