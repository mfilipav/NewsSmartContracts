from prettytable import PrettyTable
def etree_iter_path(node, tag=None, path='.'):
    if tag == "*":
        tag = None
    if tag is None or node.tag == tag:
        yield node, path
    for child in node:
        _child_path = '%s/%s' % (path, child.tag)
        for child, child_path in etree_iter_path(child, tag, path=_child_path):
            yield child, child_path
def get_element_by_tag(element, tag):
    if element.tag.endswith(tag):
        yield element
    for child in element:
        for g in get_element_by_tag(child, tag):
            yield g
def demo():
    # fet a list of all available channels
    rd = ReutersDatasource()
    tree = rd.call('channels')

    #  OUT: {'alias': 'Efm208', 'description': 'French Language News Graphics Service'}
    channels = [{'alias': c.findtext('alias'),
                 'description': c.findtext('description')}
                for c in tree.findall('channelInformation')]

    pt = PrettyTable(["Alias", "Description"])
    for c in channels:
        pt.add_row([c.get('alias'),c.get('description')])
    #print(pt)
    print("List of channels:\n\talias\tdescription\t\t\t\tprofile")
    #print("\n ".join(["\t%(alias)s\t%(description)s\t\t\t\t%(profile[@])s" % x for x in channels]))
    # fetch id's and headlines for a channel
    rd = ReutersDatasource()
    gen = (c for c in channels)     # <generator object <genexpr> at 0x10e77a150>
    for x in gen:
        alias = x.get('alias')

        print("Channel Alias: ", alias) # 24 names
        tree = rd.call('items',
                       {'channel': alias,
                        'maxAge': '7D'})
        for x in tree.findall('result'):
            print(x.findtext('id'))
        items = [{'id': c.findtext('id'),
                  'headline': c.findtext('headline'),
                  'slugline': c.findtext('slugline'),
                  'located': c.findtext('located'),
                  'previewUrl': c.findtext('previewUrl')}
                 for c in tree.findall('result') if not 'Link List' in c.findtext('headline')]
        #for i in items:
         #   if not i.get('previewUrl') is None:
          #      rd.open_Image(i.get('previewUrl'))
        # print("\n\nList of items:\n\tid\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\theadline\t\t\t\tslugline\t\t\tlocated")
        # print("\n".join(["\t%(id)s\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t%(headline)s\t\t\t\t%(slugline)s\t\t\t%(located)s"%x for x in items]))
        print("\n\n Item 1 ID: ", items[0].get('id'))


demo()
