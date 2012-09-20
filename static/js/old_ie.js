$(function(){
    if ($.browser.msie && parseInt($.browser.version, 10) < 8) {
        var errorMsgs = [
             '<div class="alert alert-block alert-error fade in" style="width:600px;position:absolute;display:block;top:30px;left:23%;">',
                '<a class="close" data-dismiss="alert" href="#">&times;</a>',
                    '<h4 class="alert-heading">'+ gettext('You are using really old browser!') +'</h4>',
                '<p style="padding-top:10px;">'+ gettext('Your IE is really out of date! We only support IE8 and above. Chrome or Firefox is strongly recommended.') +'</p>',
                '<p><a target="_blank" class="btn btn-danger" href="http://windows.microsoft.com/zh-CN/internet-explorer/products/ie-8/ie8-how-to">'+ gettext('Update IE') +'</a>&nbsp;',
                    '<a target="_blank" class="btn btn-primary" href="https://www.google.com/chrome">'+ gettext('Get Chrome') +'</a>&nbsp;',
                    '<a target="_blank" class="btn btn-info" href="http://firefox.com.cn/download/">'+ gettext('Get Firefox') +'</a></p>',
              '</div>'
                ];
        $('body').append(errorMsgs.join(''));
    }
});
