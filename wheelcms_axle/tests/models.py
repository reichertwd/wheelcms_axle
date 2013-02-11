from wheelcms_axle.content import Content, FileContent, ImageContent
from wheelcms_axle.spoke import Spoke
from wheelcms_axle.content import type_registry

from django.db import models

class Type1(Content):
    t1field = models.TextField(null=True, blank=True)


class Type1Type(Spoke):
    model = Type1


class Type2(Content):
    pass


class Type2Type(Spoke):
    model = Type2


class TestFile(FileContent):
    storage = models.FileField(upload_to="files", blank=False)


class TestFileType(Spoke):
    model = TestFile

class OtherTestFile(FileContent):
    storage = models.FileField(upload_to="files", blank=False)


class OtherTestFileType(Spoke):
    model = OtherTestFile


class TestImage(ImageContent):
    storage = models.ImageField(upload_to="images", blank=False)


class TestImageType(Spoke):
    model = TestImage

class OtherTestImage(ImageContent):
    storage = models.ImageField(upload_to="images", blank=False)


class OtherTestImageType(Spoke):
    model = OtherTestImage


type_registry.register(Type1Type)
type_registry.register(Type2Type)
type_registry.register(TestFileType)
type_registry.register(TestImageType)
type_registry.register(OtherTestFileType)
type_registry.register(OtherTestImageType)
