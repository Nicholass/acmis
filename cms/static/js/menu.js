/**
 * Плагин управления меню
 *
 * @author Underground27 <ramenky27@gmail.com>
 * @copyright 2016, Potapov studio
 * @version 1.0
 */

"use strict";

(function ( $, window, document, undefined ) {

    // Default properties definition
    var pluginName = 'acisMenu',
        pluginVersion = '1.0',
        defaults = {
            class: '',
            items: {}
        };

    /**
     * Plugin constructor
     *
     * @param {Object} element Контейнер контента
     * @param {Object} options Опции
     * @constructor
     */
    function Plugin(element, options) {
        this._name = pluginName;
        this.element = $(element);
        this.options = $.extend({}, defaults, options);
        this._defaults = defaults;

        this._init();
    }

    /**
     * Plugin initialization
     *
     * @protected
     */
    Plugin.prototype._init = function () {
        var that = this;

        if($.isEmptyObject(this.options.items)){
            return;
        }

        var menu = this._genMenu(this.options.items);

        menu
            .addClass(this.options.class)
            .prependTo(this.element);

        $(document).on('mouseenter', 'li.ext', function(event){
            that.element.find('.sub').hide();
            $(event.target).closest('li').find('.sub').show();
        });
        $(document).on('mouseleave', 'li.ext', function(event){
            $(event.target).closest('li').find('.sub').hide();
        });
        $(document).on('mouseleave', '.sub', function(event){
            var target = $(event.toElement || event.relatedTarget);
            var thatElement = $(event.target).closest('.sub').parent();
            if(target.is(thatElement)){
                return;
            }

            that.element.find('.sub').hide();
        });
    };

    Plugin.prototype._genMenu = function (items) {
        var that = this,
            list = $('<ul></ul>');

        $.each(items, function(title, item){
            var li = $('<li></li>');

            if(typeof item === "object" && item !== null){
                li.text(title);
                var submenu = that._genMenu(item);
                submenu
                    .addClass('sub')
                    .hide();

                li
                    .append(submenu)
                    .addClass('ext');
            } else {
                $('<a></a>')
                    .attr('href', item)
                    .text(title)
                    .appendTo(li);
            }

            li.appendTo(list);
        });

        return list;
    };

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName,
                    new Plugin( this, options ));
            }
        });
    }

})( jQuery, window, document );