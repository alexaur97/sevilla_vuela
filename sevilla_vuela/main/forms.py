from django import forms

class vuelos_por_destino(forms.Form):
    destino = forms.CharField(label='Destino', widget=forms.TextInput, required=True)


class vuelos_por_origen(forms.Form):
    origen = forms.CharField(label='Origen', widget=forms.TextInput, required=True)


class vuelos_por_codigo(forms.Form):
    codigo = forms.CharField(label='Codigo', widget=forms.TextInput, required=True)
