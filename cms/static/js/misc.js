$(document).ready(function(){
    "use strict";

    // Select active comment
    $(window.location.hash).addClass('selected');

    $('.comment-link').click(function (event) {
        $('.comment').removeClass('selected');
        $(event.target.hash).addClass('selected');
    });
});