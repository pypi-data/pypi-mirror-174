from django.http import HttpRequest
from django.template.context import RenderContext


class InterfaceNotFound(Exception):
    """Interface with this name was not found"""

    pass


class ITemplatePluginMixin:
    """A mixin that be inherited from to build renderable plugins.

    Use this in conjunction with :ref:`gdaps.templatetags:gdaps`
    to build plugins that are renderable in templates.
    """

    template: str = ""
    template_name: str = ""
    context: dict = {}

    def get_plugin_context(self):
        """Override this method to add custom context to the plugin.

        Per default, it only returns ``self.context``"""
        return self.context
