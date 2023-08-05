from django.template import Context


class ITemplatePluginMixin:
    """A mixin that be inherited from to build renderable plugins.

    Use this in conjunction with :ref:`gdaps.templatetags:gdaps`
    to build plugins that are renderable in templates.
    """

    template: str = ""
    template_name: str = ""
    context: dict = {}

    def get_context(self, context: Context) -> Context:
        """Override this method to add custom context to the plugin.

        :param context: the context that is passed from the template
            where this plugin is rendered.
        """
        context.update(self.context)
        return context
