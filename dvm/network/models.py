from django.db import models
from django.core.exceptions import ValidationError

class Node(models.Model):
    name = models.CharField(max_length=15, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

class Edge(models.Model):
    from_node=models.ForeignKey(Node, on_delete=models.CASCADE, related_name='ougoing_edges')
    to_node=models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')

    class Meta:
        unique_together=('from_node', 'to_node')

    def clean(self):
        if self.from_node==self.to_node:
            raise ValidationError('A node cannot have an edge pointing to itself')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.from_node.name} -> {self.to_node.name}"