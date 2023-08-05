from django.shortcuts import render


class ITemplatePluginMixin:
    """A mixin that be inherited from to build renderable plugins.

    Use this in conjunction with :ref:`gdaps.templatetags:gdaps`
    to build plugins that are renderable in templates.
    """

    template: str = ""
    template_name: str = ""
    context: dict = {}

    def get_context(self) -> dict:
        """Override this method to add custom context to the plugin."""
        return self.context
