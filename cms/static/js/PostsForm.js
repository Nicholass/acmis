$(document).ready(function() {
    "use strict";

    var tags_input = $('input[name=tags]');

    tags_input.tagsInput({
        autocomplete_url: '/ajax/tags/'
    });

    $('#id_tags_tag').change(function(event){
        var element = $(event.target);
        var value = $.trim(element.val());

        if(!value.length){
            return;
        }

        tags_input.addTag(value);
    });
});