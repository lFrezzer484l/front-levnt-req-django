from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Requirement
import requests
from django.conf import settings


# ============================================================
# CONFIGURACIÓN DE MICROSERVICIOS
# ============================================================

SERVICIOS = [
    ("FastAPI", settings.FASTAPI_API_URL),
    ("Node.js", settings.NODE_API_URL),
    ("Java", settings.JAVA_API_URL),
    ("PHP", settings.PHP_API_URL),
]


# ============================================================
# FUNCION DE RESILIENCIA
# ============================================================

def obtener_requerimientos():

    for nombre, url in SERVICIOS:

        try:

            print(f"Intentando consultar {nombre}...")

            response = requests.get(
                f"{url}/api/requirements",
                timeout=5
            )

            if response.status_code == 200:

                print(f"✓ Datos obtenidos desde {nombre}")

                return response.json()

            print(
                f"✗ {nombre} respondió con código "
                f"{response.status_code}"
            )

        except requests.exceptions.RequestException as e:

            print(f"✗ {nombre} no disponible: {e}")

    return None


def obtener_requerimiento(id):

    for nombre, url in SERVICIOS:

        try:

            print(
                f"Intentando consultar requerimiento "
                f"{id} en {nombre}..."
            )

            response = requests.get(
                f"{url}/api/requirements/{id}",
                timeout=5
            )

            # El microservicio respondio correctamente
            if response.status_code == 200:

                print(
                    f"✓ Requerimiento obtenido desde {nombre}"
                )

                return response

            # Si el servicio esta funcionando pero el
            # requerimiento no existe, no tiene sentido
            # seguir buscando en otro servicio.
            if response.status_code == 404:

                return response

            print(
                f"✗ {nombre} respondió con código "
                f"{response.status_code}"
            )

        except requests.exceptions.RequestException as e:

            print(f"✗ {nombre} no disponible: {e}")

    return None


# ============================================================
# INDEX
# ============================================================

def index(request):

    return render(
        request,
        "requerimientos/index.html"
    )


# ============================================================
# CREAR REQUERIMIENTO
# ============================================================

def nuevo(request):

    if request.method == "POST":

        datos = {
            "requester": request.POST["requester"],
            "email": request.POST["email"],
            "description": request.POST["description"],
            "requirement_type": request.POST["requirement_type"],
            "priority": request.POST["priority"],
            "titulo": request.POST["titulo"],
        }

        requests.post(
            f"{settings.LARAVEL_API_URL}/api/requirements/create",
            json=datos
        )

    return render(
        request,
        "requerimientos/nuevo.html"
    )


# ============================================================
# LISTAR REQUERIMIENTOS
# ============================================================

def lista_requerimientos(request):

    requirements = obtener_requerimientos()

    if requirements is None:

        return HttpResponse(
            "No hay ningun microservicio disponible "
            "para consultar los requerimientos.",
            status=503
        )

    return render(
        request,
        "requerimientos/lista.html",
        {
            "requirements": requirements
        }
    )


# ============================================================
# DETALLE DE REQUERIMIENTO
# ============================================================

def detalle_requerimiento(request, id):

    try:

        response = obtener_requerimiento(id)

        if response is None:

            return HttpResponse(
                "No hay ningún microservicio disponible.",
                status=503
            )

        if response.status_code == 404:

            return HttpResponse(
                "No se encontró el requerimiento"
            )

        requirement = response.json()

        return render(
            request,
            "requerimientos/detalle.html",
            {
                "requirement": requirement,
                "id": id
            }
        )

    except Exception as e:

        return HttpResponse(
            f"Error: {e}"
        )


# ============================================================
# EDITAR REQUERIMIENTO
# ============================================================

def editar_requerimiento(request, id):

    try:

        # ----------------------------------------------------
        # GET: mostrar formulario con los datos actuales
        # ----------------------------------------------------

        if request.method == "GET":

            response = obtener_requerimiento(id)

            if response is None:

                return HttpResponse(
                    "No hay ningún microservicio disponible.",
                    status=503
                )

            if response.status_code == 404:

                return HttpResponse(
                    "No se encontró el requerimiento"
                )

            if response.status_code != 200:

                return HttpResponse(
                    "Error al obtener el requerimiento"
                )

            requirement = response.json()

            return render(
                request,
                "requerimientos/editar_requerimiento.html",
                {
                    "requirement": requirement,
                    "id": id
                }
            )

        # ----------------------------------------------------
        # POST: actualizar requerimiento
        # ----------------------------------------------------

        if request.method == "POST":

            data = {
                "titulo": request.POST.get("titulo"),
                "requester": request.POST.get("requester"),
                "email": request.POST.get("email"),
                "description": request.POST.get("description"),
                "requirement_type": request.POST.get(
                    "requirement_type"
                ),
                "priority": request.POST.get("priority"),
            }

            response = requests.put(
                f"{settings.LARAVEL_API_URL}/api/requirements/{id}",
                json=data
            )

            if response.status_code == 404:

                return HttpResponse(
                    "No se encontró el requerimiento"
                )

            if response.status_code == 422:

                return HttpResponse(
                    f"Datos inválidos: {response.text}"
                )

            if response.status_code != 200:

                return HttpResponse(
                    f"Error al actualizar: {response.text}"
                )

            return redirect(
                "req:detalle_requerimiento",
                id=id
            )

    except Exception as e:

        return HttpResponse(
            f"Error: {e}"
        )


# ============================================================
# ELIMINAR REQUERIMIENTO
# ============================================================

def eliminar_requerimiento(request, id):

    try:

        if request.method != "POST":

            return HttpResponse(
                "Método no permitido",
                status=405
            )

        response = requests.delete(
            f"{settings.LARAVEL_API_URL}/api/requirements/{id}"
        )

        if response.status_code == 404:

            return HttpResponse(
                "No se encontró el requerimiento"
            )

        if response.status_code != 200:

            return HttpResponse(
                f"Error al eliminar: {response.text}"
            )

        return redirect(
            "req:lista_requerimientos"
        )

    except Exception as e:

        return HttpResponse(
            f"Error: {e}"
        )


# ============================================================
# ASISTENTE IA
# ============================================================

def asistente_ia(request):

    answer = None
    error = None

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip()

        if question:

            try:

                response = requests.post(
                    "https://backendlevantamiento-req-laravel.onrender.com/api/ai/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get("answer")

            except requests.exceptions.RequestException as e:

                error = (
                    f"Error al comunicarse con el servidor: {e}"
                )

    return render(
        request,
        "requerimientos/asistente_ia.html",
        {
            "answer": answer,
            "error": error
        }
    )