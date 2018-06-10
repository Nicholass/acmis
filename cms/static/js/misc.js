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
});