def datos_globales(request):
    return {
        'nombre_completo': request.session.get('nombre_completo','Invitado')
    }