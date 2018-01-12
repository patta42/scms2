

var PHCollection = {
    'CollectionItem' : function( fullref ){
	this._get_name_from_ref = function( ref ){
	    parts = ref.split(':');
	    return parts[parts.length-1];
	}


	// Reference to collection chooser
	this.chooser = null
    
	// stores the full reference to the item
	this.fullref = fullref
	// stores the name (last part of the full reference)
	this.name = this._get_name_from_ref(fullref);
	// If the item has an ID, it is selectable
	this.id = NaN;
	// boolean for easier testing
	this.has_id = false;
	// holds the children
	this.children = {};
	// boolean for easier testing
	this.has_children = false;

	this.is_root = false;

	// Setter for id
	this.set_id = function( id ){
	    this.id = id;
	    this.has_id = true;
	}
	// Getter for id
	this.get_id = function(){
	    return this.id;
	}
	// Getter for name
	this.get_name = function(){
	    return this.name;
	}

	// Add an item to the list of children if noone wiht this name
	// exists. 
	// returns the new or already existing item
	this.add_or_get_child = function(child){
	    
	    if (typeof this.children[child.get_name()] === typeof undefined){
		this.children[child.get_name()] = child;
		this.has_children = true;
	    }
	    return this.children[child.get_name()];
	}
    
	// fills a number with leading zeroes up to three digits
	this._leading_zeros = function (n){
	    if (n < 10){
		return '00'+n;
	    }
	    if (n < 100){
		return '0'+n;
	    }
	    return ''+n;
	}


	// outputs itself and its children in a list
	// container is the target container item,
	// depth is a number indicating the depth
	// count is a number indicating the item within this depth 
	// parent_path is the path of the parent item
	this.output_as_list = function( container, depth, count, parent_path ){

	    // default settings
	    if (typeof depth === typeof undefined){
		depth = 0;
	    }
	    if (typeof count === typeof undefined){
		count = 0;
	    } 
	    var sep = '.'
	    if (typeof parent_path === typeof undefined){
		parent_path = '';
		sep = '';
	    } 
	
	    // Make li-element
	    var element = $('<li>')
		.addClass('d'+depth)
		.data('depth',depth)
		.data('path', parent_path+sep+this._leading_zeros(count))
		.addClass('collection-item')
		.attr('id', (parent_path+sep+this._leading_zeros(count)).split('.').join('_'));
	    
	    if(this.is_root){
		element.addClass('root');
		element.html('<span class="close-indicator"><i class="fa icon-fa-times-circle"></i></span><span class="selectable-collection collection">'+this.name+'</span>');
		$('.selectable-collection', element).on('click', function(){
		    self.chooser.select($(this).parent().data('path'));
		});
		$('.close-indicator', element).on('click', function(){
		    self.chooser.indicateByPath(self.chooser.currentPath, true);
		    self.chooser.close();
		});
	    } else {

		// add id, if it has one
		if ( this.has_id){
		    $(element).data('id', this.get_id());
		    element.html((this.has_children ? '<span class="children-indicator"><i class="fa icon-fa-chevron-right"></i></span>':'')+'<span class="selectable-collection collection">'+this.name+'</span>');
		} else {
		    element.html((this.has_children ? '<span class="children-indicator"><i class="fa icon-fa-chevron-right"></i></span>':'')+'<span class="collection">'+this.name+'</span>');
		}
	    }
	    // append to container
	    container.append(element);
	    self=this;
	    $('.children-indicator', element).on('click', function(){
		self.chooser.chooseFrom($(this).parent().data('path'));
	    });
	    if (!this.is_root){
		if ( this.has_id ){
		    $('.selectable-collection', element).on('click', function(){
			self.chooser.select($(this).parent().data('path'));
		    });	
		} else {
		    $('.collection', element).on('click', function(){
			self.chooser.chooseFrom($(this).parent().data('path'));
		    });
		
		}
	    }
	    if ( this.has_children ){
		// if it has children...
		element.addClass('children')
		
		// ...append children, too
		var keys = [];
		for (var key in this.children){
		    keys.push(key);
		}
		keys.sort(
		    function(a,b){
			if (isNaN(parseInt(a)) || isNaN(parseInt(b))) {
			    if (a > b){
				return 1;
			    }
			    if (a < b){
				return -1;
			    }
			    return 0;
			} else {
			    return parseInt(b)-parseInt(a);
			}
		    }
		)
		for (var idx in keys){
		    this.children[keys[idx]].output_as_list(container, depth + 1, idx, element.data('path'));
		}
	    }
	}

	// add a child with fullref and id:
	// { 'fullref' : 'a:b:c:d:e', 'id': 19 }
	this.add_child_automatic = function( opts ){
	    var parts, child, first, remaining, proceed, chooser;
	    parts = opts['fullref'].split(':');
	    first = parts.shift();
	    remaining = parts.join(':');
	    proceed = remaining.length > 0;
	    
	    child = this.add_or_get_child(new PHCollection.CollectionItem(first));
	    
	    if (proceed) {
		child.add_child_automatic({'fullref' : remaining, 'id' : opts['id'], 'chooser': opts.chooser});
	    } else {
		child.set_id(opts['id']);
	    }
	    child.chooser = opts.chooser;
	}
    }, // closes CollectionItem
    'CollectionSelector' : function( select, enlarge, send_on_select ){
	
	var self = this;
	// reference to original select box...
	self.origSelect = $(select);
	// ...and its parent
	self.origSelectContainer = this.origSelect.parent();
	// Container Element
	self.container = $('<ul>').addClass('ph-collection-chooser');
	self.selected = $('<li>').addClass('select');
	
	// enlarge parent elemnt
	self.enlarge = enlarge;
	
	// send on select?
	self.send_on_select = send_on_select
	// Stores the current path
	self.currentPath = '';

	// Root element
	self.root = new PHCollection.CollectionItem('Alle Sammlungen');
	self.root.is_root = true;

	// function to hide original elements
	self.hideOrigs = function(){
	    self.origSelect.css('visibility','hidden').css('height','0px').css('line-height','0').css('font-size','0');
	    if(self.enlarge){
		self.origSelectContainer.css('height','0px');
		$('label[for="'+self.origSelect.attr('id')+'"]').css('width','8.333333333%');
		$('label[for="'+self.origSelect.attr('id')+'"]').parent().css('width','200%');
	    } else {
		self.container.css('margin-top','-1rem');
	    }
	    
	}


	// add the items
	self.addItems = function(){
	    $('option', self.origSelect).each(
		function(){
		    if ($(this).val() && parseInt($(this).val()) > 1){
			var opts = {
			    'fullref' : $(this).html(),
			    'id': $(this).val(),
			    'chooser' : self
			}
			self.root.add_child_automatic(opts);
		    }
		}
	    );
	}
	self.getUrlParameter = function getUrlParameter(sParam) {
	    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
	    
	    for (i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');
		
		if (sParameterName[0] === sParam) {
		    return sParameterName[1] === undefined ? true : sParameterName[1];
		}
	    }
	}	
	// hide all items
	self.hideAll = function(){
	    $('li.collection-item', self.container).hide();
	}
	// get direct children of a path 
	self.getItemsByPath = function(path){
	    // get all items starting with `path` but with one more additional level
	    var parts = path.split('.');
	    var depth = parts.length;

	    var $items = $([]);
	    $('li.collection-item', self.container).each(
		function(){
		    if ($(this).data('path').startsWith(path) && $(this).data('depth') == depth ){
			$items = $items.add('#'+$(this).attr('id'));
		    }
		}
	    );
	    return $items;
	}
	// indicate the current path 
	self.indicateByPath = function(path, lastSelected){
	    var parts = path.split('.');
	    if(lastSelected){
		self.currentPath = path;
	    }
	    // clear old values
	    self.selected.html('');
	    var curr = [], elem, indicator;
	    for (var idx in parts){
		curr[idx] = parts[idx];
		elem = $('#'+curr.join('_')+' .collection');
		
		indicator = $('<span>').html(elem.html()).data('path',curr.join('.'));
		self.selected.append(indicator);
		indicator.on('click', function(){self.chooseFrom($(this).data('path'));});
		if(lastSelected && idx == parts.length - 1){
		    indicator.addClass('selected');
		}
	    }
	}
	// show items under a given path
	self.chooseFrom = function(path){
	    self.hideAll();
	    self.indicateByPath(path);
	    $('.root', self.collector).css('top','calc(3rem + 1px)').show();
	    var c = 1;
	    self.getItemsByPath(path).each(
		function(){
		    $(this).css('top','calc('+(2*(c+1)+1)+'rem + '+c+'px)').show();
		    c++;
		}
	    )
	    return self.getItemsByPath(path);
	}
	self.select = function(path){
	    self.indicateByPath(path, true);
	    var id = path.split('.').join('_');
	    self.origSelect.val($('#'+id).data('id'));
	    if(self.send_on_select){
		self.origSelect.parents('form').submit();
	    };
	    self.close();
	}

	self.show = function(){
	    self.root.output_as_list(self.container);
	    if (self.enlarge){
		self.origSelectContainer.parent().append(self.container);
	    } else {
		self.origSelectContainer.append(self.container);
	    }
	}
	self.close = function(){
	    self.hideAll();
	}

	self.show_initial = function(){
	    var id = self.getUrlParameter('collection_id');
	    if (! id) {
		self.indicateByPath('000', true);
		return
	    }
	    $('.collection-item', self.container).each(function(){
		if($(this).data('id') === id){
		    self.indicateByPath($(this).data('path'), true);
		    return false
		}
	    });
	}

	// initial work...
	self.container.append(self.selected);
	self.hideOrigs();
	self.addItems();
	self.show()
    }
}
$(document).ready(
    function(){
	if($('#collection_chooser_collection_id').length > 0){
	    selector = new PHCollection.CollectionSelector( $('#collection_chooser_collection_id'), true, true );
	    selector.show_initial();
	}
	if ( $('#id_addimage_collection').length > 0 ){
	    addselector = new PHCollection.CollectionSelector( $('#id_addimage_collection'), false, false );
	    addselector.show_initial();
	}
	if ( $('#id_adddocument_collection').length > 0 ){
	    addselector = new PHCollection.CollectionSelector( $('#id_adddocument_collection'), false, false );
	    addselector.show_initial();
	}

//	selector.chooseFrom('000.000');
    }
)
