$(document).ready(function(){
    "use strict";

    // Select active comment
    $(window.location.hash).addClass('selected');

    $('.comment-link').click(function (event) {
        $('.comment').removeClass('selected');
        $(event.target.hash).addClass('selected');
    });

    // Blink PM button if has new
    var blink = $('.blink');
    if (blink) {
        blink.css('font-weight', 'bold');
        setInterval(function () {
            blink.each(function () {
                var element = $(this);
                if (element.css('font-weight') === '700') {
                    element.css('color', '#666');
                    element.css('font-weight', 'normal');
                } else {
                    element.css('color', '#FFF');
                    element.css('font-weight', 'bold');
                }
            });
        }, 200);
    }
});