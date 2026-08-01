from django.urls import path
from . import views


urlpatterns = [

    # LOGIN
    path(
        "",
        views.login,
        name="login"
    ),


    # PANTALLA PRINCIPAL
    path(
        "inicio/",
        views.inicio,
        name="inicio"
    ),


    # OFERTA ACADEMICA
    path(
        "oferta/",
        views.oferta,
        name="oferta"
    ),


    # KARDEX
    path(
        "kardex/",
        views.kardex,
        name="kardex"
    ),


    # HORARIO
    path(
        "horario/",
        views.horario,
        name="horario"
    ),


    # SELECCIONAR MATERIA
    path(
        "seleccionar/<int:id_grupo>/",
        views.seleccionar_materia,
        name="seleccionar"
    ),


    # INSCRIPCION
    path(
        "inscripcion/",
        views.inscripcion,
        name="inscripcion"
    ),


    # CONFIRMAR INSCRIPCION
    path(
        "confirmar-inscripcion/",
        views.confirmar_inscripcion,
        name="confirmar"
    ),


    # CERRAR SESION
    path(
        "cerrar-sesion/",
        views.cerrar_sesion,
        name="cerrar_sesion"
    ),


    # VER PAGO
    path(
        "pago/",
        views.ver_pago,
        name="ver_pago"
    ),


    # VER CODIGO
    path(
        "codigo/",
        views.ver_codigo,
        name="ver_codigo"
    ),

]