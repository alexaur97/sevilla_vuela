from django.db import models

class Vuelo(models.Model):
    ESTADOS = (
        ('Aterrizó','Aterrizo'),
        ('Programado','Programado'),
        ('En Ruta', 'En Ruta'),
    )
    codigo_vuelo = models.CharField(primary_key = True, max_length = 10)
    estado = models.CharField(max_length = 30, choices=ESTADOS)
    con_retraso = models.BooleanField()

class Salida(Vuelo):
    destino = models.CharField(max_length = 50)
    partida = models.CharField(verbose_name='Hora de salida', max_length = 10)
    aerolinea = models.ForeignKey('Aerolinea', on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo_vuelo + ': (SVQ) Sevilla - ' + self.destino

class Llegada(Vuelo):
    aerolinea = models.ForeignKey('Aerolinea', on_delete=models.CASCADE)
    origen = models.CharField(max_length = 50)
    hora_llegada = models.CharField(verbose_name='Hora de llegada', max_length = 10)

    def __str__(self):
        return self.codigo_vuelo + ': ' + self.origen +' - (SVQ) Sevilla'
    
class Salida_comp(Vuelo):
    aerolinea = models.CharField(max_length = 50)
    destino = models.CharField(max_length = 50)
    partida = models.CharField(verbose_name='Hora de salida', max_length = 10)
    operadora = models.CharField(max_length = 50)

    def __str__(self):
        return self.codigo_vuelo + ': (SVQ) Sevilla - ' + self.destino

class Llegada_comp(Vuelo):
    aerolinea = models.CharField(max_length = 50)
    origen = models.CharField(max_length = 50)
    hora_llegada = models.CharField(verbose_name='Hora de llegada', max_length = 10)
    operadora = models.CharField(max_length = 50)

    def __str__(self):
        return self.codigo_vuelo + ': ' + self.origen +' - (SVQ) Sevilla'

class Aerolinea(models.Model):
    nombre = models.CharField(max_length = 30)
    telefono = models.CharField(max_length = 15)
    logo = models.URLField()
    email = models.EmailField(null = True)
    url_web = models.URLField()
    es_habitual = models.BooleanField(verbose_name='¿Esta aerolínea opera habitualmente en Sevilla?')

    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre',)