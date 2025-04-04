function estadoMenu(menuItem) {
    const subMenu = menuItem.querySelector('ul');
    if (!subMenu) {
        console.warn("Submenu não encontrado para o item:", menuItem);
        return;
    }

    const parentUl = menuItem.parentElement;
    if (parentUl) {
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
    } else {
         console.warn("Elemento pai <ul> não encontrado para:", menuItem);
    }

    if (subMenu.style.display === "block") {
        subMenu.style.display = "none";
        menuItem.classList.remove('active');
    } else {
        subMenu.style.display = "block";
        menuItem.classList.add('active');
    }
}


// Lógica específica para os selects customizados da página Cadastrar Manutenção
document.addEventListener('DOMContentLoaded', () => {
    const customSelects = document.querySelectorAll('.custom-select');

    customSelects.forEach(selectContainer => {
        const selectedDisplay = selectContainer.querySelector('.selected');
        const optionsContainer = selectContainer.querySelector('.options');
        const optionList = selectContainer.querySelectorAll('.option');
        const hiddenInput = selectContainer.nextElementSibling;

        if (!selectedDisplay || !optionsContainer || !hiddenInput || hiddenInput.type !== 'hidden') {
            console.warn("Estrutura do custom-select incompleta ou inválida:", selectContainer);
            return;
        }

        // Placeholder visual inicial
        if (!hiddenInput.value && selectedDisplay.textContent.includes('Selecione')) {
             selectedDisplay.setAttribute('data-placeholder', 'true');
        } else {
             selectedDisplay.removeAttribute('data-placeholder');
        }

        // Abrir/fechar lista
        selectedDisplay.addEventListener('click', (event) => {
            event.stopPropagation();
            const isActive = selectContainer.classList.contains('active');
            // Fecha outros selects
            if (!isActive) {
                document.querySelectorAll('.custom-select.active').forEach(activeSelect => {
                    if (activeSelect !== selectContainer) {
                        activeSelect.classList.remove('active');
                        activeSelect.querySelector('.options').style.display = 'none';
                    }
                });
            }
            // Alterna o atual
            selectContainer.classList.toggle('active');
            optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
        });

        // Selecionar opção
        optionList.forEach(option => {
            option.addEventListener('click', () => {
                selectedDisplay.textContent = option.textContent;
                const newValue = option.dataset.value;
                selectedDisplay.dataset.value = newValue;
                hiddenInput.value = newValue;
                selectedDisplay.removeAttribute('data-placeholder');
                optionsContainer.style.display = 'none';
                selectContainer.classList.remove('active');
                hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
            });
        });
    });

    // Fechar selects ao clicar fora
    document.addEventListener('click', (event) => {
        document.querySelectorAll('.custom-select.active').forEach(activeSelect => {
             if (!activeSelect.contains(event.target)) {
                 activeSelect.classList.remove('active');
                 activeSelect.querySelector('.options').style.display = 'none';
             }
        });
    });
});

