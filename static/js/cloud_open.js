var cloudopen = {};

cloudopen.validator = {
    // http://docs.jquery.com/Plugins/Validation/Methods/email
    email: function(value, optional) {
        // contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
        return optional || /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i.test(value);
    },
    id_number: function(value) {
        if (value.length != 15 && value.length != 18) {
            return false;
        }
        return /^(\d{6})(18|19|20)?(\d{2})([01]\d)([0123]\d)(\d{3})(\d|X|x)?$/.test(value);
    },
    cellphone: function(value) {
        return /^1(3|5|8)\d{9}$/.test(value);  //only works for China
    },
};

try {
    console.info('test console info');
    console.debug('test console debug');
    console.error('test console error');
    console.log('test console log');
} catch(err){
    var emptyJSFunction = function(){};
    console = {};
    console.info = console.debug = console.error = console.log = emptyJSFunction;
}

/* TODO: rewrite form validator as JQuery plugin
(function($){
    $.fn.extend({ 
        // validate input field/form
        is_valid: function(options) {
            var defaults = {
                type: 'form',
                error_class: 'error'
            }
                 
            var options =  $.extend(defaults, options);
 
            return this.each(function() {
                var o = options;
                //code to be inserted here
                //you can access the value like this
                alert(o.padding);
            });
        }
    });
})(jQuery);
*/