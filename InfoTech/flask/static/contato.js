// === Conteúdo FINAL para contato.js ===


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
 * Preenche os campos de informação de contato na página.
 */
function preencherContatoInfo() {
    // Seleciona os campos pelo ID
    const emailInput = document.getElementById("contato-email");
    const telefoneInput = document.getElementById("contato-telefone");
    const whatsAppInput = document.getElementById("contato-whatsapp");
    const enderecoInput = document.getElementById("contato-endereco");

    // Define os valores (hardcoded neste exemplo)
    const email = "contato@infotech.com"; 
    const telefone = "(31) 3859-2394"; 
    const whatsapp = "(31) 9 9672-3311"; 
    const endereco = "Av. Contorno, 3587, Floresta, Belo Horizonte - MG, 39541-018"; 

    // Atribui os valores aos campos (eles são readonly, então isso é só para exibição)
    if (emailInput) emailInput.value = email;
    if (telefoneInput) telefoneInput.value = telefone;
    if (whatsAppInput) whatsAppInput.value = whatsapp;
    if (enderecoInput) enderecoInput.value = endereco;
}

// Executa a função para preencher as informações quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', preencherContatoInfo);

