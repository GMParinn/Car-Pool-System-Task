from django.contrib import admin
from .models import Node, Edge

class NodeAdmin(admin.ModelAdmin):

    list_display=('id', 'name', 'latitude', 'longitude',)

    search_fields=('name',)

class EdgeAdmin(admin.ModelAdmin):
    list_display=('id', 'from_node', 'to_node',)

    list_filter=('from_node', 'to_node',)

    search_fields=('from_node__name', 'to_node__name',)

admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)
