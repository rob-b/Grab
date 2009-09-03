$(document).ready(function(){
    $('#content > ul li').each(function(){
        $(this).click(function(){
            $(this).addClass('active-item read');
            $(this).siblings().removeClass('active-item');
            scroll_to($(this));

            $(this).find('form.mark-as-read').submit();
        });

        var that = $(this)
        $(this).find('a.next-item').bind('click', function(e){
            $(that).next().find('div:first').click();
            e.preventDefault();
            return false;
        });
        $(this).find('a.prev-item').bind('click', function(e){
            $(that).prev().find('div:first').click();
            e.preventDefault();
            return false;
        });
    });
    $('form.mark-as-read').each(function(){
        $(this).ajaxForm();
    })

    var input = $('#feed-list form input');
    var default_value = input.attr('value');
    input.focus(function(){
        if ($(this).attr('value') == default_value){
            $(this).attr({value: ''});
        }
    })
    input.blur(function(){
        if ($(this).attr('value') == ''){
            $(this).attr({value: default_value});
        }
    })
});

var scroll_to = function(elem){
    var target_offset = elem.offset().top;
    $('html,body').animate({scrollTop: target_offset}, 1000);
}
