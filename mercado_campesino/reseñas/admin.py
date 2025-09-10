from django.contrib import admin
from .models import Reseña

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ['producto', 'cliente', 'calificacion', 'fecha']
    list_filter = ['calificacion', 'fecha']
    search_fields = ['producto__nombre', 'cliente__usuario__first_name', 'contenido']
    ordering = ['-fecha']
