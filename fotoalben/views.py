from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render

import json, re

from wagtail.utils.pagination import paginate
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailadmin.utils import PermissionPolicyChecker, popular_tags_for_model
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.models import Collection, Page, Site
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.fields import ALLOWED_EXTENSIONS
from wagtail.wagtailimages.formats import get_image_format
from wagtail.wagtailimages.forms import ImageInsertionForm, get_image_form
from wagtail.wagtailimages.permissions import permission_policy
from wagtail.wagtailsearch import index as search_index



# Create your views here.

def get_images_json(images):
    """
    helper function: given a list of images, return the json to pass back to the
    multi-image chooser panel 
    """
    all_images = [];
    for image in images:
        preview_image = image.get_rendition('max-165x165')
        all_images.append({
            'id': image.id,
            'edit_link': reverse('wagtailimages:edit', args=(image.id,)),
            'title': image.title,
            'preview': {
                'url': preview_image.url,
                'width': preview_image.width,
                'height': preview_image.height,
            }
        })
    return json.dumps(all_images)


def get_or_create_collection( title, page_id, parent_page_id ):
    if page_id:
        page = Page.objects.get( id = page_id )
        parent_page = page.get_parent()
    else:
        parent_page = Page.objects.get( id = parent_page_id )

    ancestors = parent_page.get_ancestors( inclusive = True )
    ancestor_titles = [] 
    count = 0
    for ancestor in ancestors:
        # Do nothing for count == 0, it's the root node, we don't need that
        if count == 1:
            ancestor_titles.append(ancestor.get_site().site_name)
        if count > 1:
            ancestor_titles.append(ancestor.title)
        count += 1
    ancestor_titles.append(title)
    collection_name = ":".join(ancestor_titles)
    try:
        collection = Collection.objects.filter( name__exact = collection_name ).get()
    except Collection.DoesNotExist:
        collection = Collection()
        collection.name = collection_name
        root = Collection.get_first_root_node()
        root.add_child(instance = collection)

    return collection


def multichooser(request):
    collection_id = request.GET.get('collection_id', None)
    if not collection_id:
        album_title = request.GET.get('album_title')
        page_id = request.GET.get('page_id', None)
        parent_page_id = request.GET.get('parent_page_id', None)
        collection = get_or_create_collection( album_title, page_id, parent_page_id)
    else:
        collection = Collection.objects.get(id = collection_id)
        
    Image = get_image_model()

    if permission_policy.user_has_permission(request.user, 'add'):
        ImageForm = get_image_form(Image)
        uploadform = ImageForm(user=request.user)
    else:
        uploadform = None

    images = Image.objects.filter(collection = collection).order_by('-created_at')

    # allow hooks to modify the queryset
    for hook in hooks.get_hooks('construct_image_chooser_queryset'):
        images = hook(images, request)

    q = None
    if (
        'q' in request.GET or 'p' in request.GET or 'tag' in request.GET 
    ):
        # this request is triggered from search, pagination or 'popular tags';
        # we will just render the results.html fragment
        
        searchform = SearchForm( request.GET )
        if searchform.is_valid():
            q = searchform.cleaned_data['q']

            images = images.search(q)
            is_searching = True
        else:
            is_searching = False

            tag_name = request.GET.get('tag')
            if tag_name:
                images = images.filter(tags__name=tag_name)

        # Pagination
        paginator, images = paginate(request, images, per_page=20)

        return render(request, "fotoalben/multichooser/results.html", {
            'images': images,
            'is_searching': is_searching,
            'query_string': q,
            'will_select_format': request.GET.get('select_format')
        })
    else:
        searchform = SearchForm()
#        this_site = Site.find_for_request( request )
#        collections = Collection.objects.all()
#        if len(collections) < 2:
#            collections = None

        paginator, images = paginate(request, images, per_page=20)

        return render_modal_workflow(request, 'fotoalben/multichooser/multichooser.html', 'fotoalben/multichooser/multichooser.js', {
            'images': images,
            'uploadform': uploadform,
            'searchform': searchform,
            'is_searching': False,
            'query_string': q,
            'will_select_format': request.GET.get('select_format'),
            'popular_tags': popular_tags_for_model(Image),
            'collections': [collection],
            'collection': collection,
            'page_id' : page_id,
            'album_title' : album_title,
            'parent_page_id' : parent_page_id
        })


    
def multichooser_select( request ):
    ids = json.loads(request.GET.get('ids'))

    images = [
        get_object_or_404(get_image_model(), id= id_) for id_ in ids
    ]

    return render_modal_workflow(
        request, None, 'wagtailimages/chooser/image_chosen.js',
        {'image_json': get_images_json(images) }
    )
