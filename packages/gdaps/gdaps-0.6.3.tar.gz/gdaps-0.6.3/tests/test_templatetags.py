import pytest
from django.template import Context, Template, TemplateSyntaxError

from gdaps.api import Interface
from gdaps.api.interfaces import ITemplatePluginMixin
from gdaps.templatetags.gdaps import render_plugins

# simple template


@Interface
class IAnyItem(ITemplatePluginMixin):
    pass


class SimpleFooItem(IAnyItem):
    template = "<div>Foo</div>"


def test_render_plugin_with_simple_template():
    content = render_plugins(context=Context(), interface="IAnyItem")
    assert content == "<div>Foo</div>"


# template file
@Interface
class IAnyItemFile(ITemplatePluginMixin):
    pass


class SimpleFooItemFile(IAnyItemFile):
    template_name = "simple_foo_item.html"


def test_render_plugin_with_file_template():
    content = render_plugins(context=Context(), interface="IAnyItemFile")
    assert content == "<div>Foo - template</div>"


# simple context
@Interface
class IAnyItem2(ITemplatePluginMixin):
    pass


class SimpleFooItem2(IAnyItem2):
    template = "<div>{{context1}}</div>"


def test_render_plugin_with_simple_context():
    content = render_plugins(
        context=Context({"context1": "879d72z3d"}), interface="IAnyItem2"
    )
    assert content == "<div>879d72z3d</div>"


# templatetag rendering
def test_render_template_with_tag_no_context():
    content = Template(
        """{% load gdaps %}{% render_plugins interface='IAnyItem' %}"""
    ).render(Context())
    assert content == "<div>Foo</div>"


# simple context
@Interface
class IContextItem(ITemplatePluginMixin):
    pass


class SimpleContextItem(IContextItem):
    context = {"foo": "bar"}
    template = "<div>{{foo}}</div>"


def test_render_template_with_tag_and_context():
    content = Template(
        """{% load gdaps %}{% render_plugins interface='IContextItem' %}"""
    ).render(Context())
    assert content == "<div>bar</div>"


# get_context
@Interface
class IContextMethodItem(ITemplatePluginMixin):
    pass


class SimpleContextMethodItem(IContextMethodItem):
    def get_context(self, context):
        return {"foo": "blubb"}

    template = "<div>{{foo}}</div>"


def test_render_template_with_tag_and_context_method():
    content = Template(
        """{% load gdaps %}{% render_plugins interface='IContextMethodItem' %}"""
    ).render(Context())
    assert content == "<div>blubb</div>"


# missing interface kwarg, other instead
def test_render_template_with_wrong_interface_kwarg():
    with pytest.raises(AttributeError):
        Template(
            """{% load gdaps %}{% render_plugins foo='IContextMethodItem' %}"""
        ).render(Context())


# missing interface kwarg, arg instead
def test_render_template_with_arg_insteadof_kwarg():
    with pytest.raises(AttributeError):
        Template(
            """{% load gdaps %}{% render_plugins 'IContextMethodItem' %}"""
        ).render(Context())
