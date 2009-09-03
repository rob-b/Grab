$(document).ready(function(){
    $('#content > ul').click(function(e){
        var li, target = $(e.target);
        if (target.is('a.next-item')) {
            target.parents('li:first').next().click();
            e.preventDefault();
            return false;
        }
        else if (target.is('a.prev-item')) {
            target.parents('li:first').prev().click();
            e.preventDefault();
            return false;
        }
        else if (target.is('#content > ul li')) {
            li = target;
        }
        else if (target.parents('li').length) {
            li = target.parents('li:first');
        }
        li.addClass('active-item read');
        li.siblings().removeClass('active-item');
        scroll_to(li);

        li.find('form.mark-as-read').submit();
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
