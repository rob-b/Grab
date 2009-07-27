$(document).ready(function(){
    $('ul#post-list li').each(function(){
        $(this).click(function(){
            $(this).addClass('active-item');
            $(this).siblings().removeClass('active-item');
            scroll_to($(this));
        });
        var that = $(this)
        $(this).find('a.next').bind('click', function(e){
            scroll_to($(that).next().find('div:first'));
            e.preventDefault();
            return false;
        });
        $(this).find('a.prev').bind('click', function(e){
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

$('a[href*=#]').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
        var $target = $(this.hash);
        $target = $target.length && $target || $('[name=' + this.hash.slice(1) +']');
        if ($target.length) {
            var targetOffset = $target.offset().top;
            $('html,body').animate({scrollTop: targetOffset}, 1000);
            return false;
        }
    }
});
