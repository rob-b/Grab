$(document).ready(function(){

    search_form.init();
    item_action.init();

    $('form.mark-as-read').ajaxForm();
    $('#scrollable').scrollable({
        vertical: true,
        size: 4,
        speed: 700,
    }).mousewheel();
});

var search_form = {
    init: function(){
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
    }
}


var item_action = {
    activate_item: function(obj) {
        obj.addClass('active-item read');
        obj.siblings().removeClass('active-item');
        obj.find('form.mark-as-read').submit();
        // item_action.scroll_to(obj);
        $('#content').scrollTo(obj, {duration:1500, easing: 'easeOutExpo'});
    },
    scroll_to: function(elem){
        var target_offset = elem.offset().top;
        $('#content').animate({scrollTop: target_offset}, {duration:1500, easing: 'easeOutExpo'} );
        console.log(target_offset);
        console.log($('#content').attr('scrollTop'));
    },
    init: function(){
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
                item_action.activate_item(li);
                delay = setTimeout(function(){
                    // window.location = target.attr('href');
                    window.open(target.attr('href'));
                }, 1500);
                return false;
            }
            else{
                item_action.activate_item(li);
            }
        });
    }
}
