
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