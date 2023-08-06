from django.http import HttpRequest
from django.template.context import RenderContext, Context


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

    def get_plugin_context(self, context: Context) -> Context:
        """Override this method to add custom context to the plugin.

        :param context: the context where the plugin is rendered in.
            You can update it with own values, and return it.
            The return variable of this function will be the context
            of the rendered plugin. So if you don't update the passed
            context, but just return a new one, the plugin will not get
            access to the global context.

        Per default, it merges the plugin's ``context`` attribute into
        the given global context.
        """
        context.update(self.context)
        return context
