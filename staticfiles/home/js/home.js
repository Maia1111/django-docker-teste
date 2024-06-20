
$$(document).ready(function() {
    // Abre automaticamente os menus dropdown quando passa o mouse por cima
    $('.dropdown').hover(
        function() {
            // Quando o mouse entra no elemento .dropdown, o menu dropdown é mostrado
            $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
        }, 
        function() {
            // Quando o mouse deixa o elemento .dropdown, o menu dropdown é escondido
            $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
        }
    );
});