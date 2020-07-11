from django.db import models

class Grupo(models.Model):
    POP = "POP"
    ROCK = "RCK"
    AFROAMERICANA = "AFR"
    LATINOAMERICANA = "LAT"
    FOLK = "FLK"
    COUNTRY = "CTY"
    ELECTRONICA = "LTR"
    JAZZ = "JZZ"
    GENEROS_CHOICES = [
        (POP, 'Pop'),
        (ROCK, 'Rock'),
        (AFROAMERICANA, 'Afroamericana'),
        (LATINOAMERICANA, 'Latinoamericana'),
        (FOLK, 'Folk'),
        (COUNTRY, 'Country'),
        (ELECTRONICA, 'Electrónica'),
        (JAZZ, 'Jazz')
    ]

    nombre = models.CharField(max_length=200)
    genero = models.CharField(
        max_length=3,
        choices=GENEROS_CHOICES,
    )
    fecha_fundacion = models.DateField()
    origen = models.CharField(max_length=200)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Musico(models.Model):
    nombre = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    instrumento = models.CharField(max_length=200)
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Album(models.Model):
    titulo = models.CharField(max_length=200)
    distribuidora = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_lanzamiento = models.DateField()
    creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo