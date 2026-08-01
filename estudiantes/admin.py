from django.contrib import admin

from .models import (
    Estudiante,
    Carrera,
    Facultad,
    Docente,
    Materia,
    Grupo,
    OfertaAcademica,
    Inscripcion,
    PagoMatricula,
    CodigoAcceso
)



admin.site.register(Estudiante)

admin.site.register(Carrera)

admin.site.register(Facultad)

admin.site.register(Docente)

admin.site.register(Materia)

admin.site.register(Grupo)

admin.site.register(OfertaAcademica)

admin.site.register(Inscripcion)

admin.site.register(PagoMatricula)

admin.site.register(CodigoAcceso)