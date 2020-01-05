from django.db import models

class Salida(models.Model):
    ESTADOS = (
        ('Aterrizó','Aterrizo'),
        ('Programado','Programado'),
        ('En Ruta', 'En Ruta'),
    )
    codigo_vuelo = models.CharField(primary_key = True, max_length = 10)
    aerolinea = models.ForeignKey('Aerolinea', on_delete=models.CASCADE)
    destino = models.CharField(max_length = 50)
    partida = models.CharField(verbose_name='Hora de salida', max_length = 10)
    estado = models.CharField(max_length = 30, choices=ESTADOS)
    con_retraso = models.BooleanField()

    def __str__(self):
        return self.codigo_vuelo + ': (SVQ) Sevilla - ' + self.destino
    
    class Meta:
        ordering = ('partida',)

class Llegada(models.Model):
    ESTADOS = (
        ('Aterrizó','Aterrizo'),
        ('Programado','Programado'),
        ('En Ruta', 'En Ruta'),
    )
    codigo_vuelo = models.CharField(primary_key = True, max_length = 10)
    aerolinea = models.ForeignKey('Aerolinea', on_delete=models.CASCADE)
    origen = models.CharField(max_length = 50)
    llegada = models.CharField(verbose_name='Hora de llegada', max_length = 10)
    estado = models.CharField(max_length = 30, choices=ESTADOS)
    con_retraso = models.BooleanField()

    def __str__(self):
        return self.codigo_vuelo + ': ' + self.origen +' - (SVQ) Sevilla'
    
    class Meta:
        ordering = ('llegada',)

class Aerolinea(models.Model):
    nombre = models.CharField(max_length = 30)

    def __str__(self):
        return self.nombre