$(document).ready(function(){
  $('.fotoalbum-karussell').slick({
      adaptiveHeight: true,
      lazyLoad: 'ondemand'
  });
});

$(document).ready(function(){
  $('.video-karussell').slick({
      adaptiveHeight: true,
      lazyLoad: 'ondemand',
      dots: true
  });
  $('.video-karussell').on('beforeChange', function(event, slick, currentSlide, nextSlide){
      console.log(currentSlide);
      //$('video', currentSlide).pause();
  });
});
