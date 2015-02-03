
var timer;

    var main = function() {
        $('.frame').hover(
            function(){
                sliderin = $('.description',this);
                timer = setTimeout(function(){sliderin.show(200);}, 600);
            },
            function() {
                clearTimeout(timer);
                $('.description',this).hide('slow');
            }
        );

        $('.learnmore').hover(
            function(){
              $('span',this).show()
            },
            function(){
                $('span',this).hide()
            }
        );
    };

$(document).ready(main);