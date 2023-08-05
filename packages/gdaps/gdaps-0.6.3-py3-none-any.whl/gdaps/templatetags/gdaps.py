from django import template
from django.template import Template, loader, Context
from django.utils.safestring import mark_safe

from ..api import InterfaceRegistry

register = template.Library()


@register.simple_tag(takes_context=True)
def render_plugins(context: Context, *args, **kwargs) -> str:
    """A template tag that renders all plugins that implement the given interface.

    The plugins must either have a ``template`` str that is rendered directly,
    or a ``template_name`` attribute with the name of the template file.
    """
    content = ""
    if not "interface" in kwargs:
        raise AttributeError(
            "Please provide an 'interface' to render as attribute to 'render_plugin'."
        )
    for plugin in InterfaceRegistry.get(kwargs["interface"]):
        context.update(plugin.get_context(context))
        if hasattr(plugin, "template") and plugin.template:
            content += Template(template_string=plugin.template).render(context)
        else:
            template = loader.get_template(template_name=plugin.template_name).template
            content += template.render(context)
    return mark_safe(content)
