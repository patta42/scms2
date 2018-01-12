function hasClass(el, className) {
  if (el.classList)
    return el.classList.contains(className)
  else
    return !!el.className.match(new RegExp('(\\s|^)' + className + '(\\s|$)'))
}

function addClass(el, className) {
  if (el.classList)
    el.classList.add(className)
  else if (!hasClass(el, className)) el.className += " " + className
}

function removeClass(el, className) {
  if (el.classList)
    el.classList.remove(className)
  else if (hasClass(el, className)) {
    var reg = new RegExp('(\\s|^)' + className + '(\\s|$)')
    el.className=el.className.replace(reg, ' ')
  }
}

offsetTops = {};
var e = document.getElementsByClassName('fixme');
var c = 0;
for (var i=0; i< e.length; ++i){
    if (e[i].getAttribute('id') === null){
	e[i].setAttribute('id', 'fixed'+c.toString());
	c++;
    }
    offsetTops[e[i].getAttribute('id')] = e[i].offsetTop;
}


function scrollFunction(){ 
    var offset_els = document.getElementsByClassName('fixed');
    var offset = 0;
    for (var i=0; i<offset_els.length; ++i){
	offset += offset_els[i].offsetHeight;
    }
    var e = document.getElementsByClassName('fixme');
    for (var i=0; i < e.length; ++i){
	if(!hasClass(e[i], 'fixed')){
	    if (window.scrollY >= offsetTops[e[i].getAttribute('id')] - offset) {
		addClass(e[i], 'fixed');
	    }
	}
	else {
	    if (window.scrollY < offsetTops[e[i].getAttribute('id')] - offset) {
		removeClass(e[i], 'fixed');
	    }

	}

    }
}

var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
var AddEvent = window[eventMethod];
var scrollEvent = eventMethod == "attachEvent" ? "onscroll" : "scroll";

AddEvent(scrollEvent, scrollFunction, false);
