function(modal) {
    var searchUrl = $('form.image-search', modal.body).attr('action');

    /* currentTag stores the tag currently being filtered on, so that we can
    preserve this when paginating */
    var currentTag;
    window.multichooser = {}
    window.multichooser.selected_ids=[];
    function ajaxifyLinks (context) {
        $('.listing a', context).click(function() {
	    var id = $(this).data('imageid');
	    var pos = $.inArray(id, window.multichooser.selected_ids);
	    if ( pos < 0 ){
		window.multichooser.selected_ids.push( id );
	    } 
	    else {
		window.multichooser.selected_ids.splice( pos, 1 );
	    }
	    $(this).toggleClass('selected');
	    console.log(window.multichooser.selected_ids);
            return false;
        });

        $('.pagination a', context).click(function() {
            var page = this.getAttribute("data-page");
            setPage(page);
            return false;
        });

	$('.addbutton a', context).click(function() {
	    $('#upload-list form').each(
		function(){
		    id = $(this).attr('action').split('/')[4];
		    if ($.inArray(window.multichooser.selected_ids, id) < 0){
			window.multichooser.selected_ids.push( id );
		    }
		}
	    );
	    options = {'ids' : JSON.stringify(window.multichooser.selected_ids)};
    modal.loadUrl(this.href, options);
	    return false;
	});
    }

    function fetchResults(requestData) {
        $.ajax({
            url: searchUrl,
            data: requestData,
            success: function(data, status) {
                $('#image-results').html(data);
                ajaxifyLinks($('#image-results'));
		$.each(window.multichooser.selected_ids, function(idx, val){
		    $("[data-imageid="+val+"]").addClass('selected');
		});
            }
        });
    }

    function search() {
        /* Searching causes currentTag to be cleared - otherwise there's
        no way to de-select a tag */
        currentTag = null;
        fetchResults({
            q: $('#id_q').val(),
            collection_id: $('#collection_chooser_collection_id').val()
        });
        return false;
    }

    function setPage(page) {
        params = {p: page};
        if ($('#id_q').val().length){
            params['q'] = $('#id_q').val();
        }
        if (currentTag) {
            params['tag'] = currentTag;
        }
        params['collection_id'] = $('#collection_chooser_collection_id').val();
        fetchResults(params);
        return false;
    }

    ajaxifyLinks(modal.body);

/*    $('#id_tags', modal.body).tagit({
        autocomplete: {source: "{{ autocomplete_url|addslashes }}"}
    });
*/

    $('#fileupload').fileupload({
        dataType: 'html',
        sequentialUploads: true,
        dropZone: $('.drop-zone'),
        acceptFileTypes: window.fileupload_opts.accepted_file_types,
        maxFileSize: window.fileupload_opts.max_file_size,
        previewMinWidth:150,
        previewMaxWidth:150,
        previewMinHeight:150,
        previewMaxHeight:150,
        messages: {
            acceptFileTypes: window.fileupload_opts.errormessages.accepted_file_types,
            maxFileSize: window.fileupload_opts.errormessages.max_file_size
        },
        add: function(e, data) {
            $('.messages').empty();
            var $this = $(this);
            var that = $this.data('blueimp-fileupload') || $this.data('fileupload')
            var li = $($('#upload-list-item').html()).addClass('upload-uploading')
            var options = that.options;

            $('#upload-list').append(li);
            data.context = li;

            data.process(function() {
                return $this.fileupload('process', data);
            }).always(function() {
                data.context.removeClass('processing');
                data.context.find('.left').each(function(index, elm) {
                    $(elm).append(escapeHtml(data.files[index].name));
                });

                data.context.find('.preview .thumb').each(function(index, elm) {
                    $(elm).addClass('hasthumb')
                    $(elm).append(data.files[index].preview);
                });

            }).done(function() {
                data.context.find('.start').prop('disabled', false);
                if ((that._trigger('added', e, data) !== false) &&
                        (options.autoUpload || data.autoUpload) &&
                        data.autoUpload !== false) {
                    data.submit()
                }
            }).fail(function() {
                if (data.files.error) {
                    data.context.each(function(index) {
                        var error = data.files[index].error;
                        if (error) {
                            $(this).find('.error_messages').text(error);
                        }
                    });
                }
            });
        },

        processfail: function(e, data) {
            var itemElement = $(data.context);
            itemElement.removeClass('upload-uploading').addClass('upload-failure');
        },

        progress: function(e, data) {
            if (e.isDefaultPrevented()) {
                return false;
            }

            var progress = Math.floor(data.loaded / data.total * 100);
            data.context.each(function() {
                $(this).find('.progress').addClass('active').attr('aria-valuenow', progress).find('.bar').css(
                    'width',
                    progress + '%'
                ).html(progress + '%');
            });
        },

        progressall: function(e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#overall-progress').addClass('active').attr('aria-valuenow', progress).find('.bar').css(
                'width',
                progress + '%'
            ).html(progress + '%');

            if (progress >= 100) {
                $('#overall-progress').removeClass('active').find('.bar').css('width', '0%');
            }
        },

        done: function(e, data) {
            var itemElement = $(data.context);
            var response = $.parseJSON(data.result);

            if (response.success) {
                itemElement.addClass('upload-success')

                $('.right', itemElement).append(response.form);
            } else {
                itemElement.addClass('upload-failure');
                $('.right .error_messages', itemElement).append(response.error_message);
            }

        },

        fail: function(e, data) {
            var itemElement = $(data.context);
            var errorMessage = $('.server-error', itemElement);
            $('.error-text', errorMessage).text(data.errorThrown);
            $('.error-code', errorMessage).text(data.jqXHR.status);

            itemElement.addClass('upload-server-error');
        },

        always: function(e, data) {
            var itemElement = $(data.context);
            itemElement.removeClass('upload-uploading').addClass('upload-complete');
        }
    });


    $(document).bind('drop dragover', function(e) {
        e.preventDefault();
    });
    $('form.image-upload', modal.body).submit(function() {
        var formdata = new FormData(this);

        if ($('#id_title', modal.body).val() == '') {
            var li = $('#id_title', modal.body).closest('li');
            if (!li.hasClass('error')) {
                li.addClass('error');
                $('#id_title', modal.body).closest('.field-content').append('<p class="error-message"><span>This field is required.</span></p>')
            }
            setTimeout(cancelSpinner, 500);
        } else {
            $.ajax({
                url: this.action,
                data: formdata,
                processData: false,
                contentType: false,
                type: 'POST',
                dataType: 'text',
                success: function(response){
                    modal.loadResponseText(response);
                }
            });
        }

        return false;
    });

    $('form.image-search', modal.body).submit(search);

    $('#id_q').on('input', function() {
        clearTimeout($.data(this, 'timer'));
        var wait = setTimeout(search, 200);
        $(this).data('timer', wait);
    });
    $('#collection_chooser_collection_id').change(search);
    $('a.suggested-tag').click(function() {
        currentTag = $(this).text();
        $('#id_q').val('');
        fetchResults({
            'tag': currentTag,
            collection_id: $('#collection_chooser_collection_id').val()
        });
        return false;
    });
}
/**
    {% url 'wagtailadmin_tag_autocomplete' as autocomplete_url %}

    /* Add tag entry interface (with autocompletion) to the tag field of the image upload form */
/*

    // Redirect users that don't support filereader
    if (!$('html').hasClass('filereader')) {
        document.location.href = window.fileupload_opts.simple_upload_url;
        return false;
    }

    // prevents browser default drag/drop



    // ajax-enhance forms added on done()
    $('#upload-list').on('submit', 'form', function(e) {
        var form = $(this);
        var itemElement = form.closest('#upload-list > li');

        e.preventDefault();

        $.post(this.action, form.serialize(), function(data) {
            if (data.success) {
                var statusText = $('.status-msg.update-success').text();
                addMessage('success', statusText);
                itemElement.slideUp(function() {$(this).remove()});
            } else {
                form.replaceWith(data.form);

                // run tagit enhancement on new form
                $('.tag_field input', form).tagit(window.tagit_opts);
            }
        });
    });

    $('#upload-list').on('click', '.delete', function(e) {
        var form = $(this).closest('form');
        var itemElement = form.closest('#upload-list > li');

        e.preventDefault();

        var CSRFToken = $('input[name="csrfmiddlewaretoken"]', form).val();

        $.post(this.href, {csrfmiddlewaretoken: CSRFToken}, function(data) {
            if (data.success) {
                itemElement.slideUp(function() {$(this).remove()});
            }
        });
    });
});
*/
