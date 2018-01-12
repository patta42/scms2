from django import template

register = template.Library()

@register.inclusion_tag(
    'scms2/blocks/sitemap_content.html')
def sitemap( page ):
    return { 'pages' : page.get_children().live() }


class ListItem():
    def __init__( self, content = None ):
        self.content = content
        self.children = []
        self.has_children = False
    def add_child(self, child):
        self.has_children = True
        self.children.append(child)
    def get_last_child(self):
        return self.children[-1]
    


@register.inclusion_tag(
    'scms2/blocks/ol_block_for_list.html')
def complex_list( values ):
    last_items = {
        '-1': None,
        '0' : None,
        '1' : None,
        '2' : None
    }
    
    root = ListItem()
    last_items['-1'] = root

    for item in values:
        level = int(item.get('level'))
        it = ListItem(item.get('content'))
        last_items[str(level-1)].add_child(it)
        last_items[str(level)] = it;
        
    return { 'items' : root.children }
