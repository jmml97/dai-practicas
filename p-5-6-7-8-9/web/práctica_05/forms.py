from django import forms

from .models import Grupo, Musico, Album

class GrupoForm(forms.ModelForm):

    class Meta:
        model = Grupo
        fields = ('nombre', 'genero', 'fecha_fundacion', 'origen',)

class MusicoForm(forms.ModelForm):

    class Meta:
        model = Musico
        fields = ('nombre', 'grupo', 'fecha_nacimiento', 'instrumento',)

class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ('titulo', 'distribuidora', 'grupo', 'fecha_lanzamiento',)