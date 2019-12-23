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

    // Show new comments
    filter_new_comments();
    $(window).on('hashchange', function () {
        filter_new_comments();
    });

    // Clear user search result after form reset
    $('.search-form-inline input[type=reset]').click(function (e) {
        e.preventDefault();
        var url = location.href.split('?');
        if (url.length) location.href = url[0];
    });
});

function filter_new_comments() {
    var comments = $('.comment');
    var comments_all_link = $('#сomments_new');

    if (window.location.hash === '#comments_new') {
        var new_comments = comments.filter('.new');
        var old_comments = comments.not('.new');
        if (new_comments.length && old_comments.length) {
            old_comments.hide();
            comments_all_link.show();
        }

        $([document.documentElement, document.body]).animate({
            scrollTop: $('#comments').offset().top
        }, 0);
    } else {
        comments.show();
        comments_all_link.hide();
    }
}
