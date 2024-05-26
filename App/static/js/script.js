"use strict"

// NAVBAR DROPDOWN ANIMATION
$(document).ready(function () {
    // Kur klikohet në elementin me klasën 'dropdown-toggle'
    $('.dropdown-toggle').click(function () {
        // Kalo nëpër të gjitha elementet në dropdown
        $(this).next('.dropdown-menu').slideToggle();
    });
});