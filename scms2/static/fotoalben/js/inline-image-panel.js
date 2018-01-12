function buildExpandingImageFormset(prefix, opts) {
    if (!opts) {
        opts = {};
    }

    var addButton = $('#' + prefix + '-ADD');
    var formContainer = $('#' + prefix + '-FORMS');
    var totalFormsInput = $('#' + prefix + '-TOTAL_FORMS');
    var formCount = parseInt(totalFormsInput.val(), 10);

    if (opts.onInit) {
        for (var i = 0; i < formCount; i++) {
            opts.onInit(i);
        }
    }

    var emptyFormTemplate = document.getElementById(prefix + '-EMPTY_FORM_TEMPLATE');
    if (emptyFormTemplate.innerText) {
        emptyFormTemplate = emptyFormTemplate.innerText;
    } else if (emptyFormTemplate.textContent) {
        emptyFormTemplate = emptyFormTemplate.textContent;
    };
    get_parent_page_id = function() {
	var re = /\d+/;
	if (window.location.pathname.indexOf('/pages/add/') > -1 ){
	    var res = window.location.pathname.match(re);
	    return res[0];
	} 
	else {
	    return null;
	}
    };
    get_page_id = function() {
	var re = /pages\/\d+\/edit\/$/;
	var m = window.location.pathname.match(re);
	if (m){
	    var re2 = /\d+/;
	    var res = m[0].match(re2);
	    return res[0];
	    
	} 
	else {
	    return null;
	}
    };
    addButton.add_elem = function() {
        if (addButton.hasClass('disabled')) return false;
        var newFormHtml = emptyFormTemplate
            .replace(/__prefix__/g, formCount)
            .replace(/<-(-*)\/script>/g, '<$1/script>');
        formContainer.append(newFormHtml);
        if (opts.onAdd) opts.onAdd(formCount);
        if (opts.onInit) opts.onInit(formCount);

        formCount++;
        totalFormsInput.val(formCount);
	return formCount;
    };
    addButton.click(function(){
	if ($('#id_title').val().trim() == ''){
	    alert('Bitte zuerst einen Titel angeben');
	    return
	}
	ModalWorkflow({
	    url: window.chooserUrls.inlineImageChooser,
	    urlParams: { 
		'album_title' : $('#id_title').val().trim(),
		'parent_page_id' : get_parent_page_id(),
		'page_id' : get_page_id()
	    },
	    method : 'POST',
	    responses: {
		imageChosen: function(imageData) {
		    imgs = imageData;
		    $.each(imgs, function(idx, imgData){
			counter = addButton.add_elem();
			previewImage = $('img', '#inline_child_'+prefix.substr(3)+'-'+(counter-1));
			chooserElement = previewImage.parents('.chooser');
			input = chooserElement.next('input');
			input.val(imgData.id);


			previewImage.attr({
			    src: imgData.preview.url,
			    width: imgData.preview.width,
			    height: imgData.preview.height,
			    alt: imgData.title
			});
			chooserElement.removeClass('blank');
		    });
		    //editLink.attr('href', imageData.edit_link);
		}
	    }
	});
    });
}

function InlineImagePanel(opts) {
    var self = {};

    self.setHasContent = function() {
        if ($('> li', self.formsUl).not('.deleted').length) {
            self.formsUl.parent().removeClass('empty');
        } else {
            self.formsUl.parent().addClass('empty');
        }
    };

    self.initChildControls = function(prefix) {
        var childId = 'inline_child_' + prefix;
        var deleteInputId = 'id_' + prefix + '-DELETE';

        //mark container as having children to identify fields in use from those not
        self.setHasContent();

        $('#' + deleteInputId + '-button').click(function() {
            /* set 'deleted' form field to true */
            $('#' + deleteInputId).val('1');
            $('#' + childId).addClass('deleted').slideUp(function() {
                self.updateMoveButtonDisabledStates();
                self.updateAddButtonState();
                self.setHasContent();
            });
        });

        if (opts.canOrder) {
            $('#' + prefix + '-move-up').click(function() {
                var currentChild = $('#' + childId);
                var currentChildOrderElem = currentChild.find('input[name$="-ORDER"]');
                var currentChildOrder = currentChildOrderElem.val();

                /* find the previous visible 'inline_child' li before this one */
                var prevChild = currentChild.prev(':visible');
                if (!prevChild.length) return;
                var prevChildOrderElem = prevChild.find('input[name$="-ORDER"]');
                var prevChildOrder = prevChildOrderElem.val();

                // async swap animation must run before the insertBefore line below, but doesn't need to finish first
                self.animateSwap(currentChild, prevChild);

                currentChild.insertBefore(prevChild);
                currentChildOrderElem.val(prevChildOrder);
                prevChildOrderElem.val(currentChildOrder);

                self.updateMoveButtonDisabledStates();
            });

            $('#' + prefix + '-move-down').click(function() {
                var currentChild = $('#' + childId);
                var currentChildOrderElem = currentChild.find('input[name$="-ORDER"]');
                var currentChildOrder = currentChildOrderElem.val();

                /* find the next visible 'inline_child' li after this one */
                var nextChild = currentChild.next(':visible');
                if (!nextChild.length) return;
                var nextChildOrderElem = nextChild.find('input[name$="-ORDER"]');
                var nextChildOrder = nextChildOrderElem.val();

                // async swap animation must run before the insertAfter line below, but doesn't need to finish first
                self.animateSwap(currentChild, nextChild);

                currentChild.insertAfter(nextChild);
                currentChildOrderElem.val(nextChildOrder);
                nextChildOrderElem.val(currentChildOrder);

                self.updateMoveButtonDisabledStates();
            });
        }

        /* Hide container on page load if it is marked as deleted. Remove the error
         message so that it doesn't count towards the number of errors on the tab at the
         top of the page. */
        if ($('#' + deleteInputId).val() === '1') {
            $('#' + childId).addClass('deleted').hide(0, function() {
                self.updateMoveButtonDisabledStates();
                self.updateAddButtonState();
                self.setHasContent();
            });

            $('#' + childId).find('.error-message').remove();
        }
    };

    self.formsUl = $('#' + opts.formsetPrefix + '-FORMS');

    self.updateMoveButtonDisabledStates = function() {
        if (opts.canOrder) {
            var forms = self.formsUl.children('li:visible');
            forms.each(function(i) {
                $('ul.controls .inline-child-move-up', this).toggleClass('disabled', i === 0).toggleClass('enabled', i !== 0);
                $('ul.controls .inline-child-move-down', this).toggleClass('disabled', i === forms.length - 1).toggleClass('enabled', i != forms.length - 1);
            });
        }
    };

    self.updateAddButtonState = function() {
        if (opts.maxForms) {
            var forms = self.formsUl.children('li:visible');
            var addButton = $('#' + opts.formsetPrefix + '-ADD');

            if (forms.length >= opts.maxForms) {
                addButton.addClass('disabled');
            } else {
                addButton.removeClass('disabled');
            }
        }
    };

    self.animateSwap = function(item1, item2) {
        var parent = self.formsUl;
        var children = parent.children('li:visible');

        // Apply moving class to container (ul.multiple) so it can assist absolute positioning of it's children
        // Also set it's relatively calculated height to be an absolute one, to prevent the container collapsing while its children go absolute
        parent.addClass('moving').css('height', parent.height());

        children.each(function() {
            // console.log($(this));
            $(this).css('top', $(this).position().top);
        }).addClass('moving');

        // animate swapping around
        item1.animate({
            top:item2.position().top
        }, 200, function() {
            parent.removeClass('moving').removeAttr('style');
            children.removeClass('moving').removeAttr('style');
        });

        item2.animate({
            top:item1.position().top
        }, 200, function() {
            parent.removeClass('moving').removeAttr('style');
            children.removeClass('moving').removeAttr('style');
        });
    };

    buildExpandingImageFormset(opts.formsetPrefix, {
        onAdd: function(formCount) {
            var newChildPrefix = opts.emptyChildFormPrefix.replace(/__prefix__/g, formCount);
            self.initChildControls(newChildPrefix);
            if (opts.canOrder) {
                /* NB form hidden inputs use 0-based index and only increment formCount *after* this function is run.
                Therefore formcount and order are currently equal and order must be incremented
                to ensure it's *greater* than previous item */
                $('#id_' + newChildPrefix + '-ORDER').val(formCount + 1);
            }

            self.updateMoveButtonDisabledStates();
            self.updateAddButtonState();

            if (opts.onAdd) opts.onAdd();
        }
    });

    return self;
}
