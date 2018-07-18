$(document).ready(function(){
    "use strict";

    //Переключатель языка
    $('.langBtn').click(function (event) {
        var element = $(event.target).parent().parent();
        if(element.hasClass('selected')){
            return false;
        }

        element.siblings().removeClass('selected');
        element.addClass('selected');

        var languageCode = element.attr('id');
        $('input[name=language]').val(languageCode);
        $('.langSwitcher').submit();

        return false;
    });

    $("[data-fancybox]").fancybox({
	    buttons: [
            "zoom",
            "share",
            "download",
            "close"
        ],
    });

    resize_handle();

    //Handlers for mobile devices
    $(window).resize(function () {
        console.log('resize');
        resize_handle();
    });

    //Show PM notify popup if user first see this in 1 hour
    var cookies = getCookies();
    if (!cookies.hasOwnProperty('hidePopup')) {
        var pmPopup = $("#pm-notification");
        pmPopup.fadeIn("slow");
        pmPopup.click(function(){
            pmPopup.fadeOut("slow");

            var date = new Date(new Date().getTime() + 60 * 1000 * 60);
            document.cookie = "hidePopup=true; path=/; expires=" + date.toUTCString()
        });
    }

    //Resize elements depends on screen dimensions
    function resize_handle() {
        $('.breadcrumbs li.current').off('click');
        $('.langBtn.selected').off('click');

        if($(window).width() < 600) {
            $('.breadcrumbs li.current').click(function () {
                $('.breadcrumbs li:not(.current)').toggle("slow");
            });

            $('.langBtn.selected').click(function () {
                $('.langBtn:not(.selected)').toggle("slow");
            });
        }
    }

    //Return object of cookies
    function getCookies () {
        var cookies = {};

        document.cookie.split('; ').map(function (item) {
        var pair = item.split('=');
            if (pair.length > 1){
                cookies[pair[0]] = pair[1]
            }
        });

        return cookies;
    }
});