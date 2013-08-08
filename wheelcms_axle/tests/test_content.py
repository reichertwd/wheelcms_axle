import pytest

from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.models import User

from wheelcms_axle.node import Node, NodeInUse
from wheelcms_axle.content import Content
from wheelcms_axle.tests.models import Type1, Type2, TypeM2M


class TestContent(object):
    """ Test content / content-node related stuff """

    def test_duplicate_content(self, client):
        """ two content objects cannot point to the same node """
        root = Node.root()
        child1 = root.add("n1")
        Type1(node=child1).save()
        pytest.raises(IntegrityError, lambda: Type1(node=child1).save())

    def test_node_content(self, client):
        """ get the actual content instance through the node """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1(node=child1)
        c1.save()
        child2 = root.add("n2")
        c2 = Type2(node=child2)
        c2.save()

        assert child1.content() == c1
        assert child2.content() == c2

    def test_node_set(self, client):
        """ test the node.set method """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1)
        c1 = Type1.objects.get(pk=c1.pk)  ## get updated state
        assert child1.content() == c1
        assert c1.node == child1

    def test_node_set_base(self, client):
        """ test the node.set method  with Content instance """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1.content_ptr)

        assert child1.content() == c1

    def test_node_set_replace(self, client):
        """ test the node.set method """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1)
        c2 = Type2()
        c2.save()
        old = child1.set(c2, replace=True)

        assert child1.content() == c2
        assert old == c1

    def test_node_set_inuse(self, client):
        """ a node can not hold two content items """
        root = Node.root()
        child1 = root.add("n1")
        c1 = Type1()
        c1.save()
        child1.set(c1)
        c2 = Type2()
        c2.save()
        pytest.raises(NodeInUse, child1.set, c2)

    def test_content_default(self, client):
        """ test defaults on new content """
        c1 = Type1()
        c1.save()
        assert c1.created
        assert c1.modified
        assert c1.publication
        assert c1.expire > timezone.now()
        assert not c1.navigation

    def test_content_default_update(self, client):
        """ test defaults on updated content """
        c1 = Type1()
        c1.save()
        created = c1.created
        modified = c1.modified
        c1.save()
        assert c1.modified > modified
        assert c1.created == created

    def test_absolute_url(self, client):
        """ the absolute url for a content object is that of its node """
        root = Node.root()
        n = root.add("path").add("sub")
        c1 = Type1(node=n).save()
        assert c1.get_absolute_url() == n.get_absolute_url()

    def test_absolute_url_unattached(self, client):
        """ the absolute url for unattached content is None """
        c1 = Type1().save()
        assert c1.get_absolute_url() is None

    ## copy/paste

    def test_copy_content_simple(self, client):
        c1 = Type1(title="hello", state="visible", t1field="orig").save()
        c2 = c1.copy()
        assert c1 != c2
        assert c1.title == c2.title
        assert c1.state == c2.state
        assert c1.t1field == c2.t1field

        c2.t1field = "copy"
        c2.save()

        ## verify the inheritance magic works as expected
        bases = Content.objects.all().order_by("id")
        assert bases.count() == 2
        orig = bases[0]
        copy = bases[1]

        assert orig != copy
        assert orig.type1 != copy.type1

        t1s = Type1.objects.all()
        assert t1s[0].t1field != t1s[1].t1field

    def test_copy_content_owner(self, client):
        owner = User.objects.get_or_create(username="owner")[0]
        c1 = Type1(title="hello", owner=owner).save()
        c2 = c1.copy()
        assert c1 != c2
        assert c1.owner == c2.owner

    def test_copy_content_m2m(self, client):
        m2m1 = TypeM2M().save()
        m2m2 = TypeM2M().save()
        c1 = TypeM2M().save()

        c1.m2m = [m2m1, m2m2]

        c2 = c1.copy()

        assert set(c2.m2m.all()) == set((m2m1, m2m2))
