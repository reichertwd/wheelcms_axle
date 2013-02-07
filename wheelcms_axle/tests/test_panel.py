"""
    The panel method in the Main handler is responsible for filling the
    link/image selection/upload browser. It does a lot of stuff and needs
    some tests.
"""
from ..models import Node

from .models import Type1
from wheelcms_spokes.image import Image
from wheelcms_spokes.file import File

from .test_handler import MainHandlerTestable, superuser_request

from django.core.files.uploadedfile import SimpleUploadedFile

storage = SimpleUploadedFile("foo.png", 
                             'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
                             '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
class TestPanel(object):
    """
        Test different panel invocation scenario's
    """
    def test_unattached_root_link(self, client):
        """
            A single root with no content attached. Should allow
            upload of content
        """
        root = Node.root()
        request = superuser_request("/", method="GET")
        handler = MainHandlerTestable(request=request, instance=root)
        panels = handler.panels(path="", mode="link")
        assert len(panels['panels']) == 1
        assert panels['path'] == '/'
        
        # import pytest; pytest.set_trace()
        crumbs = panels['crumbs']['context']['crumbs']
        assert len(crumbs) == 1
        assert crumbs[0]['path'] == ''

        ## inspect crumbs
        root_panel = panels['panels'][0]
        assert root_panel['context']['selectable']
        assert root_panel['context']['instance']['addables']

    def setup_root_children(self):
        """ setup some children """
        root = Node.root()
        i1 = Type1(node=root.add("type1")).save()
        i2 = Image(storage=storage, node=root.add("image")).save()
        i3 = File(storage=storage, node=root.add("file")).save()

        return root, i1.node, i2.node, i3.node

    def test_root_children_link(self, client):
        """ panel in link mode, anything is selectable """
        self.setup_root_children()

        request = superuser_request("/", method="GET")
        handler = MainHandlerTestable(request=request, instance=Node.root())
        panels = handler.panels(path="", mode="link")
        assert len(panels['panels']) == 1
        assert panels['path'] == '/'
        
        root_panel = panels['panels'][0]
        assert root_panel['context']['selectable']
        assert root_panel['context']['instance']['addables']
        children = root_panel['context']['instance']['children']
        assert len(children) == 3
        assert set(x['path'] for x in children) == set(('/type1', '/image', '/file'))
        for c in children:
            assert c['selectable']
            assert not c['selected']

    def test_root_children_image(self, client):
        """ panel in link image, ony image-ish content is selectable """
        self.setup_root_children()

        request = superuser_request("/", method="GET")
        handler = MainHandlerTestable(request=request, instance=Node.root())
        panels = handler.panels(path="", mode="image")
        assert len(panels['panels']) == 1
        assert panels['path'] == '/'
        
        root_panel = panels['panels'][0]
        assert root_panel['context']['selectable']
        assert root_panel['context']['instance']['addables']
        children = root_panel['context']['instance']['children']
        assert len(children) == 3
        assert set(x['path'] for x in children) == set(('/type1', '/image', '/file'))
        for c in children:
            if c['meta_type'] == 'image':
                assert c['selectable']
            else:
                assert not c['selectable']
            assert not c['selected']

    def test_subpanel_image(self, client):
        """
            handle subcontent, results in two panels
        """
        root, _, image1, _ = self.setup_root_children()

        request = superuser_request("/image1", method="GET")
        handler = MainHandlerTestable(request=request, instance=image1)
        panels = handler.panels(path="/image", mode="image")
        assert len(panels['panels']) == 2
        assert panels['path'] == '/image'
        
        crumbs = panels['crumbs']['context']['crumbs']
        assert len(crumbs) == 2
        assert crumbs[0]['path'] == ''
        assert crumbs[1]['path'] == '/image'

        root_panel = panels['panels'][0]
        children = root_panel['context']['instance']['children']
        assert len(children) == 3
        for c in children:
            if c['meta_type'] == 'image':
                assert c['selectable']
                assert c['selected']
            else:
                assert not c['selectable']
                assert not c['selected']

        image_panel = panels['panels'][1]
        assert not image_panel['context']['instance']['children']
        assert not image_panel['context']['instance']['addables']
