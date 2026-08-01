from django.shortcuts import render, redirect
from datetime import date
import random
import string

from estudiantes.models import (
    Estudiante,
    PagoMatricula,
    CodigoAcceso,
    OfertaAcademica,
    Materia,
    Grupo,
    Inscripcion,
    Horario
)



# =========================
# LOGIN
# =========================

def login(request):

    if request.method == "POST":

        codigo = request.POST.get("codigo_sis")
        password = request.POST.get("password")


        try:

            estudiante = Estudiante.objects.get(
                cod_sis_est=codigo
            )


            if password == "123456":

                request.session["codigo_sis"] = codigo

                return redirect("/inicio/")


            else:

                return render(
                    request,
                    "autenticacion/login.html",
                    {
                        "error":"Contraseña incorrecta"
                    }
                )


        except Estudiante.DoesNotExist:


            return render(
                request,
                "autenticacion/login.html",
                {
                    "error":"Código SIS incorrecto"
                }
            )


    return render(
        request,
        "autenticacion/login.html"
    )



# =========================
# INICIO
# =========================

def inicio(request):


    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    pago = PagoMatricula.objects.filter(

        cod_sis_est=estudiante

    ).first()



    codigo_acceso = CodigoAcceso.objects.filter(

        cod_sis_est=estudiante

    ).first()



    # =========================
    # GENERAR CODIGO ACCESO
    # =========================

    if not codigo_acceso:


        clave = ''.join(

            random.choices(

                string.ascii_uppercase + string.digits,

                k=6

            )

        )



        ultimo_codigo = CodigoAcceso.objects.all().order_by(

            "-id_codigo"

        ).first()



        if ultimo_codigo:

            nuevo_id = ultimo_codigo.id_codigo + 1

        else:

            nuevo_id = 1




        codigo_acceso = CodigoAcceso.objects.create(

            id_codigo=nuevo_id,

            cod_sis_est=estudiante,

            usuario=estudiante.cod_sis_est,

            clave_acceso=clave,

            fecha_generacion=date.today(),

            estado="Activo",

            id_pago=pago

        )




    return render(

        request,

        "autenticacion/inicio.html",

        {

            "estudiante": estudiante,

            "pago": pago,

            "codigo_acceso": codigo_acceso

        }

    )





# =========================
# OFERTA ACADEMICA
# =========================

def oferta(request):


    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    materias = Materia.objects.all()



    for materia in materias:


        materia.grupos = Grupo.objects.filter(

            id_materia=materia

        )


        materia.inscrita = Inscripcion.objects.filter(

            cod_sis_est=estudiante,

            id_grupo__id_materia=materia

        ).exists()



    return render(

        request,

        "autenticacion/oferta.html",

        {

            "materias": materias,

            "estudiante": estudiante

        }

    )





# =========================
# KARDEX
# =========================

def kardex(request):


    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    inscripciones = Inscripcion.objects.filter(

        cod_sis_est=estudiante

    )



    return render(

        request,

        "autenticacion/kardex.html",

        {

            "estudiante": estudiante,

            "inscripciones": inscripciones

        }

    )





# =========================
# SELECCIONAR MATERIA
# =========================

def seleccionar_materia(request, id_grupo):


    request.session["grupo_seleccionado"] = id_grupo


    return redirect(

        "/inscripcion/"

    )





# =========================
# INSCRIPCION
# =========================

def inscripcion(request):


    codigo = request.session.get(

        "codigo_sis"

    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    grupo = None



    grupo_id = request.session.get(

        "grupo_seleccionado"

    )



    if grupo_id:


        grupo = Grupo.objects.get(

            id_grupo=grupo_id

        )



    return render(

        request,

        "autenticacion/inscripcion.html",

        {

            "estudiante": estudiante,

            "grupo": grupo

        }

    )





# =========================
# CONFIRMAR INSCRIPCION
# =========================

def confirmar_inscripcion(request):


    codigo = request.session.get(

        "codigo_sis"

    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    grupo_id = request.session.get(

        "grupo_seleccionado"

    )



    if not grupo_id:

        return redirect("/oferta/")



    grupo = Grupo.objects.get(

        id_grupo=grupo_id

    )



    oferta = OfertaAcademica.objects.filter(

        id_carrera=estudiante.id_carrera

    ).first()



    # VALIDAR SI YA EXISTE INSCRIPCIÓN

    existe = Inscripcion.objects.filter(

        cod_sis_est=estudiante,

        id_grupo=grupo

    ).exists()



    if existe:


        return render(

            request,

            "autenticacion/inscripcion_exitosa.html",

            {

                "estudiante": estudiante,

                "grupo": grupo,

                "mensaje":
                "Esta materia ya se encuentra inscrita"

            }

        )





    # GENERAR ID AUTOMÁTICO

    ultimo = Inscripcion.objects.all().order_by(

        "-id_inscripcion"

    ).first()



    if ultimo:

        nuevo_id = ultimo.id_inscripcion + 1

    else:

        nuevo_id = 1





    inscripcion = Inscripcion.objects.create(

        id_inscripcion=nuevo_id,

        cod_sis_est=estudiante,

        id_grupo=grupo,

        id_oferta=oferta,

        fecha_inscripcion=date.today(),

        estado_materia="Inscrita",

        nota_final=None

    )





    return render(

        request,

        "autenticacion/inscripcion_exitosa.html",

        {

            "estudiante": estudiante,

            "grupo": grupo,

            "inscripcion": inscripcion,

            "mensaje":
            "Inscripción realizada correctamente"

        }

    )
# =========================
# HORARIO ESTUDIANTE
# =========================

def horario(request):

    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    inscripciones = Inscripcion.objects.filter(

        cod_sis_est=estudiante

    )



    horarios = []



    for inscripcion in inscripciones:

        lista = Horario.objects.filter(

            id_grupo=inscripcion.id_grupo

        )


        for h in lista:

            horarios.append(h)



    # ORDENAR HORARIO

    orden_dias = {

        "Lunes": 1,
        "Martes": 2,
        "Miércoles": 3,
        "Jueves": 4,
        "Viernes": 5,
        "Sábado": 6

    }



    horarios.sort(

        key=lambda x: (

            orden_dias.get(x.dia, 7),

            x.hora_inicio

        )

    )



    return render(

        request,

        "autenticacion/horario.html",

        {

            "estudiante": estudiante,

            "horarios": horarios

        }

    )
# =========================
# CERRAR SESION
# =========================

def cerrar_sesion(request):

    request.session.flush()

    return redirect("/")

# =========================
# VER PAGO MATRICULA
# =========================

def ver_pago(request):

    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    pago = PagoMatricula.objects.filter(

        cod_sis_est=estudiante

    ).first()



    return render(

        request,

        "autenticacion/pago.html",

        {

            "estudiante": estudiante,

            "pago": pago

        }

    )
# =========================
# VER CODIGO DE ACCESO
# =========================

def ver_codigo(request):

    codigo = request.session.get(
        "codigo_sis"
    )


    if not codigo:

        return redirect("/")



    estudiante = Estudiante.objects.get(

        cod_sis_est=codigo

    )



    codigo_acceso = CodigoAcceso.objects.filter(

        cod_sis_est=estudiante

    ).first()



    return render(

        request,

        "autenticacion/codigo.html",

        {

            "estudiante": estudiante,

            "codigo_acceso": codigo_acceso

        }

    )