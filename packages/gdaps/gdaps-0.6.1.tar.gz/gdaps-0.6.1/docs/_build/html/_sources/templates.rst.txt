GDAPS template support
======================

Plugins usually provide not only interfaces for the backend, but also for the frontend. GDAPS supports plugin rendering in Django templates, which have to follow a certain pattern. Define your interface in the providing app, e.g. as usually in ``.api.interfaces``, and let it inherit ``ITemplatePluginMixin``. Don't forget to document your interface, so that the implementor knows what to expect.

    .. code-block:: python

        # main_app.api.interfaces.py

        from gdaps.api import Interface
        from gdaps.api.interfaces import ITemplatePluginMixin

        @Interface
        class AnyItem(ITemplatePluginMixin):
            """Any list item, must contain a <li> element as root."""

This defines the plugin hook your plugins can implement. ``ITemplatePluginMixin`` has two attributes:

.. _template:

template
    A string that is rendered as Template. For simple & small templates, e.g. one-liners. If this attribute is present, it is used.

.. _template_name:

template_name
    The usual django-like template name, where to find the template file within the ``templates`` directory, like "my_app/any_item.html"
    This attribute is used, if no ``template`` attribute is provided.

.. _context:

context
    a dict that provides context for template rendering.

.. _get_context:

def get_context(self)
    Override this method to add custom context to the plugin. Per default just uses ``self.context``.

Now, in your other plugins, create the implementation:

  .. code-block:: python

    # in plugin A

    from gdaps.api import Interface
    from gdaps.api.interfaces import ITemplatePluginMixin

    class SayFooItem(AnyItem):
        template = "<li>Foo!</li>


    # in plugin B
    ...

    class SayBarItem(AnyItem):
        template = "<li>Bar!</li>

Now, in your main app's template, just render the plugins using the ``render_plugins`` tag, with the interface name as parameter:

  .. code-block:: django

    {% load gdaps %}

    <h1>Plugin sandbox</h1>
    <ul>
        {% render_plugins interface="IAnyItem" %}
    </ul>

That's all. GDAPS finds any plugins implementing this interface and renders them, one after another, in place.

As said before, the plugin templates can contain anything you like, not only ``<li>`` elements. U can use it for select options, cards on a dashboard, or whole page contents - it's up to you.
