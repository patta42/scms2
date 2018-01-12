var initPhotoswipe = function( selector ){
    var getSlidesFromAlbum = function(album){
	// returns the slides from an album
	var slides = [], 
            pic, size, tmp, title;
	$('a', album).each( 
	    function(){
		if ($('img', $(this)).length > 0){
		    pic = $('img', $(this))[0];
		} else {
		    pic = false;
		}
		size = $(this).data('size').split('x');
		tmp = {
		    src : $(this).attr('href'),
		    w : parseInt(size[0], 10),
		    h : parseInt(size[1], 10),
		}
		if (pic){
		    var title = $(pic).attr('title');
		    if (typeof title !== typeof undefined && title !== false) {
			tmp['title'] = title;
		    }
		    tmp['thumb'] = pic;
		    tmp['msrc'] = $(pic).attr('src');
		}
		slides.push(tmp);
	    }
	);
	return slides;
    };
    
    var openPhotoswipe = function(idx, album, fromURL){
	// opens Photoswipe
	var slides = getSlidesFromAlbum(album);
	var options = {
	    index : idx,
	    showHideOpacity:true,
	    getThumbBoundsFn: function(index) {
                var thumbnail = slides[index].thumb;
		if (thumbnail){
                    pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
                    rect = thumbnail.getBoundingClientRect(); 
                    return {x:rect.left, y:rect.top + pageYScroll, w:rect.width};
		} else {
		    return false;
		}
	    }
	}

	var gallery = new PhotoSwipe(
	    $('.pswp')[0],
	    PhotoSwipeUI_Default,
	    slides,
	    options
	);
	gallery.init();
    };
    
    var setCallbacks = function( elem ){
	// sets the callbacks for the links 
	$('a', $(elem)).each( function() {
	    $(this).on('click', function(evt){
		// prevent the normal link execution
		evt.preventDefault();
		// index of the image clicked
		var idx = $(this).data('index');
		// Call open
		openPhotoswipe(idx, elem, false);
	    });
	});
    };

    var photoswipeParseHash = function() {
        var hash = window.location.hash.substring(1),
        params = {};
	
        if(hash.length < 5) {
            return params;
        }
	
        var vars = hash.split('&');
        for (var i = 0; i < vars.length; i++) {
            if(!vars[i]) {
                continue;
            }
            var pair = vars[i].split('=');  
            if(pair.length < 2) {
                continue;
            }           
            params[pair[0]] = pair[1];
        }
	
        if(params.gid) {
            params.gid = parseInt(params.gid, 10);
        }
	
        return params;
    };


    // Set callbacks for links

    $(selector).each(function(){
	setCallbacks(this);
    });
    var hashData = photoswipeParseHash();
    if(hashData.pid && hashData.gid) {
        openPhotoswipe( hashData.pid ,  $(selector)[0], true );
    }
}
$(document).ready(
    function(){
	initPhotoswipe('.fotoalbum');
    }
);
