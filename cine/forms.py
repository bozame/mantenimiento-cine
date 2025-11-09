# cine/forms.py
from django import forms
from .models import Salas

class SalaForm(forms.ModelForm):
    class Meta:
        model = Salas
        fields = ['numero', 'capacidad', 'id_estado_func']
        labels = {
            'numero': 'Número de sala',
            'capacidad': 'Capacidad',
            'id_estado_func': 'Estado funcional',
        }
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_estado_func': forms.Select(attrs={'class': 'form-select'}),
        }
