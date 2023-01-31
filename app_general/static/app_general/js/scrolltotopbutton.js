// SCROLL TOP BTN
$(document).ready(function(){ 
    $(window).scroll(function(){ 
        if ($(this).scrollTop() > 100) { 
            $('#scrolltopbutton').fadeIn(); 
        } else { 
            $('#scrolltopbutton').fadeOut(); 
        } 
    }); 
    $('#scrolltopbutton').click(function(){ 
        $("html, body").animate({ scrollTop: 0 }, 100); 
        return false; 
    }); 
});

