$.fn.TextAreaResizer=function(){
	return this.each(
		function(){
			$(this).keypress(function(event) {
				if (((event.keyCode == 13) || (event.keyCode == 10)) && (event.ctrlKey == true)) this.form.submit.click();
				
				this.rows = countLines(this.value,this.cols) +1;
			});
		}
	);
};
/**
 * ScrollView - jQuery plugin 0.1
 *
 * This plugin supplies contents view by grab and drag scroll.
 *
 * Copyright (c) 2009 Toshimitsu Takahashi
 *
 * Released under the MIT license.
 *
 * == Usage =======================
 *   // apply to block element.
 *   $("#map").scrollview();
 *   
 *   // with setting grab and drag icon urls.
 *   //   grab: the cursor when mouse button is up.
 *   //   grabbing: the cursor when mouse button is down.
 *   //
 *   $("#map".scrollview({
 *     grab : "images/openhand.cur",
 *     grabbing : "images/closedhand.cur"
 *   });
 * ================================
 */
(function() {
    function ScrollView(){ this.initialize.apply(this, arguments) }
    ScrollView.prototype = {
        initialize: function(container, config){
                // setting cursor.
                var gecko = navigator.userAgent.indexOf("Gecko/") != -1;
                var opera = navigator.userAgent.indexOf("Opera/") != -1;
                var mac = navigator.userAgent.indexOf("Mac OS") != -1;
                if (opera) {
                    this.grab = "default";
                    this.grabbing = "move";
                } else if (!(mac && gecko) && config) {
                    if (config.grab) {
                       this.grab = "url(\"" + config.grab + "\"),default";
                    }
                    if (config.grabbing) {
                       this.grabbing = "url(" + config.grabbing + "),move";
                    }
                } else if (gecko) {
                    this.grab = "default";
                    this.grabbing = "-moz-grabbing";
                } else {
                    this.grab = "default";
                    this.grabbing = "move";
                }
                
                // Get container and image.
                this.m = $(container);
                this.i = this.m.children().css("cursor", this.grab);
                
                this.isgrabbing = false;
                
                // Set mouse events.
                var self = this;
                this.i.mousedown(function(e){
                        self.startgrab();
                        this.xp = e.pageX;
                        this.yp = e.pageY;
                        return false;
                }).mousemove(function(e){
                        if (!self.isgrabbing) return true;
                        self.scrollTo(this.xp - e.pageX, this.yp - e.pageY);
                        this.xp = e.pageX;
                        this.yp = e.pageY;
                        return false;
                })
                .mouseout(function(){ self.stopgrab() })
                .mouseup(function(){ self.stopgrab() })
                .dblclick(function(){
                        var _m = self.m;
                        var off = _m.offset();
                        var dx = this.xp - off.left - _m.width() / 2;
                        if (dx < 0) {
                                dx = "+=" + dx + "px";
                        } else {
                                dx = "-=" + -dx + "px";
                        }
                        var dy = this.yp - off.top - _m.height() / 2;
                        if (dy < 0) {
                                dy = "+=" + dy + "px";
                        } else {
                                dy = "-=" + -dy + "px";
                        }
                        _m.animate({ scrollLeft:  dx, scrollTop: dy },
                                "normal", "swing");
                });
                
                this.centering();
        },
        centering: function(){
                var _m = this.m;
                var w = this.i.width() - _m.width();
                var h = this.i.height() - _m.height();
                _m.scrollLeft(w / 2).scrollTop(h / 2);
        },
        startgrab: function(){
                this.isgrabbing = true;
                this.i.css("cursor", this.grabbing);
        },
        stopgrab: function(){
                this.isgrabbing = false;
                this.i.css("cursor", this.grab);
        },
        scrollTo: function(dx, dy){
                var _m = this.m;
                var x = _m.scrollLeft() + dx;
                var y = _m.scrollTop() + dy;
                _m.scrollLeft(x).scrollTop(y);
        }
    };
    
    jQuery.fn.scrollview = function(config){
        return this.each(function(){
            new ScrollView(this, config);
        });
    };
})(jQuery);

/*!
 * jQuery Cookie Plugin v1.3
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2011, Klaus Hartl
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.opensource.org/licenses/GPL-2.0
 */
(function ($, document, undefined) {

	var pluses = /\+/g;

	function raw(s) {
		return s;
	}

	function decoded(s) {
		return decodeURIComponent(s.replace(pluses, ' '));
	}

	var config = $.cookie = function (key, value, options) {

		// write
		if (value !== undefined) {
			options = $.extend({}, config.defaults, options);

			if (value === null) {
				options.expires = -1;
			}

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setDate(t.getDate() + days);
			}

			value = config.json ? JSON.stringify(value) : String(value);

			return (document.cookie = [
				encodeURIComponent(key), '=', config.raw ? value : encodeURIComponent(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// read
		var decode = config.raw ? raw : decoded;
		var cookies = document.cookie.split('; ');
		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			if (decode(parts.shift()) === key) {
				var cookie = decode(parts.join('='));
				return config.json ? JSON.parse(cookie) : cookie;
			}
		}

		return null;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) !== null) {
			$.cookie(key, null, options);
			return true;
		}
		return false;
	};

})(jQuery, document);


$(document).ready(
	function(){$('textarea#fld1').TextAreaResizer();
		$('textarea#fld2').TextAreaResizer();
		$('textarea#fld3').TextAreaResizer();
		$('textarea#fld4').TextAreaResizer();
		$('textarea#fld5').TextAreaResizer();
		$('textarea#fld6').TextAreaResizer();
		$('textarea#fld7').TextAreaResizer();
		$('textarea#fld8').TextAreaResizer();
		$('textarea#fld9').TextAreaResizer();
		$('textarea#fld10').TextAreaResizer();
		$('textarea#fld11').TextAreaResizer();
		$('iframe.resizable').TextAreaResizer();
		
		var clientWidth = $(window).width();

		if (clientWidth >= 1600) {
			var max_width = '100%';
		}
		if (clientWidth < 1600) {
			var max_width = (parseInt(clientWidth) - 340) + 'px';
		}
		
		jQuery('span.postimg').each(function() {
			var div = jQuery('<div style="max-width:'+max_width+'; overflow:auto;"></div>');
			jQuery(this).wrap(div);
			jQuery(this).parent().scrollview();
		});
			
	}
);

function countLines(strtocount, cols) {
	var hard_lines = 5;
	var last = 0;
	while ( true ) {
		last = strtocount.indexOf("\n", last+1);
		hard_lines ++;
		if ( last == -1 ) break;
	}
	var soft_lines = Math.round(strtocount.length / (cols-1));
	var hard = eval("hard_lines  " + unescape("%3e") + "soft_lines;");
	if ( hard ) soft_lines = hard_lines;
	return soft_lines;
}

function toggleAnnouncement(id) {
	$('#announcement-content').toggle();
	$('#announcement-header').toggleClass('inactive');
	
	
	if ($('#announcement-content').is(':visible')) {
		$.cookie("announcement", null);
		$('#toggle-announcement').html('[-]');
	} else {
		$.cookie("announcement", id, { expires : 365 });
		$('#toggle-announcement').html('[+]');
	}
}
