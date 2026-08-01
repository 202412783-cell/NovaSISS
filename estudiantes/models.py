from django.db import models


# =========================
# FACULTAD
# =========================

class Facultad(models.Model):

    id_facultad = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )


    class Meta:
        managed = False
        db_table = "FACULTAD"


    def __str__(self):
        return self.nombre



# =========================
# CARRERA
# =========================

class Carrera(models.Model):

    id_carrera = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    id_facultad = models.ForeignKey(
        Facultad,
        models.DO_NOTHING,
        db_column="id_facultad"
    )


    class Meta:
        managed = False
        db_table = "CARRERA"


    def __str__(self):
        return self.nombre



# =========================
# ESTUDIANTE
# =========================

class Estudiante(models.Model):

    cod_sis_est = models.CharField(
        primary_key=True,
        max_length=15
    )

    nombres_est = models.CharField(
        max_length=50
    )

    apellidos_est = models.CharField(
        max_length=50
    )

    ci_est = models.CharField(
        max_length=15
    )

    fecha_nacimiento_est = models.DateField()

    genero_est = models.CharField(
        max_length=20
    )

    correo_institucional = models.CharField(
        max_length=100
    )

    telefono_est = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    datos_biograficos = models.TextField(
        blank=True,
        null=True
    )

    id_carrera = models.ForeignKey(
        Carrera,
        models.DO_NOTHING,
        db_column="id_carrera"
    )


    class Meta:
        managed = True
        db_table = "estudiante"


    def __str__(self):

        return (
            self.nombres_est
            + " "
            + self.apellidos_est
        )



# =========================
# DOCENTE
# =========================

class Docente(models.Model):

    id_docente = models.IntegerField(
        primary_key=True
    )

    nombres = models.CharField(
        max_length=50
    )

    apellidos = models.CharField(
        max_length=50
    )


    class Meta:
        managed = False
        db_table = "DOCENTE"


    def __str__(self):

        return (
            self.nombres
            + " "
            + self.apellidos
        )



# =========================
# MATERIA
# =========================

class Materia(models.Model):

    id_materia = models.IntegerField(
        primary_key=True
    )

    nombre = models.CharField(
        max_length=100
    )

    creditos = models.IntegerField()

    id_oferta = models.IntegerField()


    class Meta:
        managed = False
        db_table = "MATERIA"


    def __str__(self):

        return self.nombre



# =========================
# GRUPO
# =========================

class Grupo(models.Model):

    id_grupo = models.IntegerField(
        primary_key=True
    )

    id_materia = models.ForeignKey(
        Materia,
        models.DO_NOTHING,
        db_column="id_materia"
    )

    id_docente = models.ForeignKey(
        Docente,
        models.DO_NOTHING,
        db_column="id_docente"
    )

    cupo_maximo = models.IntegerField()


    class Meta:
        managed = False
        db_table = "GRUPO"


    def __str__(self):

        return self.id_materia.nombre



# =========================
# OFERTA ACADEMICA
# =========================

class OfertaAcademica(models.Model):

    id_oferta = models.IntegerField(
        primary_key=True
    )

    id_carrera = models.ForeignKey(
        Carrera,
        models.DO_NOTHING,
        db_column="id_carrera"
    )

    gestion = models.CharField(
        max_length=10
    )

    periodo = models.CharField(
        max_length=20
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    estado = models.CharField(
        max_length=20
    )


    class Meta:
        managed = False
        db_table = "OFERTA_ACADEMICA"



# =========================
# PAGO MATRICULA
# =========================

class PagoMatricula(models.Model):

    id_pago = models.IntegerField(
        primary_key=True
    )

    cod_sis_est = models.ForeignKey(
        Estudiante,
        models.DO_NOTHING,
        db_column="cod_sis_est"
    )

    id_oferta = models.ForeignKey(
        OfertaAcademica,
        models.DO_NOTHING,
        db_column="id_oferta"
    )

    nro_transaccion = models.CharField(
        max_length=50
    )

    fecha_pago = models.DateField()

    monto_pago = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    tipo_pago = models.CharField(
        max_length=30
    )

    estado_validacion = models.CharField(
        max_length=20
    )


    class Meta:
        managed = False
        db_table = "PAGO_MATRICULA"



# =========================
# CODIGO ACCESO
# =========================

class CodigoAcceso(models.Model):

    id_codigo = models.IntegerField(
        primary_key=True
    )

    cod_sis_est = models.ForeignKey(
        Estudiante,
        models.DO_NOTHING,
        db_column="cod_sis_est"
    )

    usuario = models.CharField(
        max_length=50
    )

    clave_acceso = models.CharField(
        max_length=100
    )

    fecha_generacion = models.DateField()

    estado = models.CharField(
        max_length=20
    )

    id_pago = models.ForeignKey(
        PagoMatricula,
        models.DO_NOTHING,
        db_column="id_pago",
        blank=True,
        null=True
    )


    class Meta:
        managed = False
        db_table = "CODIGO_ACCESO"



# =========================
# INSCRIPCION
# =========================

class Inscripcion(models.Model):

    id_inscripcion = models.IntegerField(
        primary_key=True
    )

    cod_sis_est = models.ForeignKey(
        Estudiante,
        models.DO_NOTHING,
        db_column="cod_sis_est"
    )

    id_grupo = models.ForeignKey(
        Grupo,
        models.DO_NOTHING,
        db_column="id_grupo"
    )

    id_oferta = models.ForeignKey(
        OfertaAcademica,
        models.DO_NOTHING,
        db_column="id_oferta"
    )

    fecha_inscripcion = models.DateField()

    estado_materia = models.CharField(
        max_length=20
    )

    nota_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True
    )


    class Meta:
        managed = False
        db_table = "INSCRIPCION"


    def __str__(self):

        return (
            self.id_grupo.id_materia.nombre
            + " - "
            + self.cod_sis_est.nombres_est
        )



# =========================
# AULA
# =========================

class Aula(models.Model):

    id_aula = models.IntegerField(
        primary_key=True
    )

    nombre_aula = models.CharField(
        max_length=20
    )

    capacidad = models.IntegerField()

    edificio = models.CharField(
        max_length=50
    )


    class Meta:
        managed = False
        db_table = "AULA"



# =========================
# HORARIO
# =========================

class Horario(models.Model):

    id_horario = models.IntegerField(
        primary_key=True
    )

    id_grupo = models.ForeignKey(
        Grupo,
        models.DO_NOTHING,
        db_column="id_grupo"
    )

    id_aula = models.ForeignKey(
        Aula,
        models.DO_NOTHING,
        db_column="id_aula"
    )

    dia = models.CharField(
        max_length=20
    )

    hora_inicio = models.TimeField()

    hora_fin = models.TimeField()


    class Meta:
        managed = False
        db_table = "HORARIO"