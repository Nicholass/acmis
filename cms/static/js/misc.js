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
});