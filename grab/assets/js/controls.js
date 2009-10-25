$(document).ready(function(){
    var delay;
    $('#content > ul').click(function(e){
        clearTimeout(delay);
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

        if (target.is('a')) {
            e.preventDefault();
            activate_item(li);
            delay = setTimeout(function(){
                window.location = target.attr('href');
            }, 1500);
            return false;
        }
        else{
            activate_item(li);
        }
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

    $('#scrollable').scrollable({
        vertical: true,
        size: 4,
        speed: 700,
    }).mousewheel();
});

var activate_item = function(obj) {
    obj.addClass('active-item read');
    obj.siblings().removeClass('active-item');
    obj.find('form.mark-as-read').submit();
    scroll_to(obj);
}

var scroll_to = function(elem){
    var target_offset = elem.offset().top;
    $('html,body').animate({scrollTop: target_offset}, {duration: 1000, easing: 'swing'} );
}
