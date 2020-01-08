from django import forms

class vuelos_por_destino(forms.Form):
    destino = forms.CharField(label='Destino', widget=forms.TextInput, required=True)