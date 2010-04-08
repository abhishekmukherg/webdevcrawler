from django import template

register = template.Library()

try:
    from django.views.decorators.csrf import csrf_protect
except ImportError:
    @register.tag
    def csrf_token(parser, token):
        class Foo(template.Node):
            def render(self, context):
                return ''
        return Foo()

