$(document).ready(function(){
    $('ul#post-list li').each(function(){
        $(this).click(function(){
            $(this).addClass('active-item');
            $(this).siblings().removeClass('active-item');
            scroll_to($(this));
        });
        var that = $(this)
        $(this).find('a.next-item').bind('click', function(e){
            scroll_to($(that).next().find('div:first'));
            e.preventDefault();
            return false;
        });
        $(this).find('a.prev-item').bind('click', function(e){
            scroll_to($(that).prev().find('div:first'));
            e.preventDefault();
            return false;
        });
    });
});

var scroll_to = function(elem){
    var target_offset = elem.offset().top;
    $('html,body').animate({scrollTop: target_offset}, 1000);
}
