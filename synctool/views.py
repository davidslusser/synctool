"""
Description: this file provides project-level views
"""

from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='SyncTool APIs')
    return response.Response(generator.get_schema(request=request))


class RegisterUser(generic.CreateView):
    """ add a new user to NextHost """
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register_user.html'
