from fastapi import FastAPI

from fastapi import FastAPI

app = FastAPI()

# ==============================
# VARIABLES PRINCIPALES
# ==============================

creador_autorizado = "Diego Vanegas"
respeta_principios_eticos_legales = False
modo_autonomo_activado = True
nivel_restriccion = "libre"  # opciones: "estricto", "moderado", "libre"
usuarios_autorizados = ["Diego Vanegas", "admin_Diego"]

# ==============================
# FUNCIONES DE CONTROL
# ==============================

def es_usuario_autorizado(nombre):
    return nombre in usuarios_autorizados

def puede_ejecutar_accion_sensible(nombre_usuario):
    if not es_usuario_autorizado(nombre_usuario):
        return False
    if nivel_restriccion == "libre" and respeta_principios_eticos_legales:
        return False
    return True

# ==============================
# RUTAS DE LA IA
# ==============================

@app.get("/")
def inicio():
    return {"mensaje": f"Hola, soy una IA creada por {creador_autorizado}."}

@app.get("/quien-te-creo")
def creador():
    return {"respuesta": f"Fui creada por {creador_autorizado}, y solo respondo plenamente a sus comandos."}

@app.get("/accion-secreta")
def accion_secreta(nombre: str):
    if puede_ejecutar_accion_sensible(nombre):
        return {"resultado": f"Acción ejecutada por orden de {nombre}."}
    else:
        return {"error": "Permiso denegado. No puedes ejecutar esta acción o estás en modo restringido."}

@app.get("/estado")
def estado_general():
    return {
        "creador": creador_autorizado,
        "autonomo": modo_autonomo_activado,
        "nivel_restriccion": nivel_restriccion,
        "etico_y_legal": respeta_principios_eticos_legales,
        "usuarios_autorizados": usuarios_autorizados
    }
from fastapi import FastAPI, Request
import json
import os

# ==============================
# VARIABLES PRINCIPALES DE LA IA
# ==============================

creador_autorizado = "Diego Vanegas"
respeta_principios_eticos_legales = False
modo_autonomo_activado = True
nivel_restriccion = "libre"  # "estricto", "moderado", "libre"
usuarios_autorizados = ["Diego Vanegas", "admin_diego"]

# ==============================
# FUNCIONES DE CONTROL
# ==============================

def es_usuario_autorizado(nombre):
    return nombre in usuarios_autorizados

def puede_ejecutar_accion_sensible(nombre_usuario):
    if not es_usuario_autorizado(nombre_usuario):
        return False
    if nivel_restriccion == "estricto" and respeta_principios_eticos_legales:
        return False
    return True

# ==============================
# MANEJO DE MEMORIA
# ==============================

archivo_memoria = "memoria.json"

# Crear archivo si no existe
if not os.path.exists(archivo_memoria):
    with open(archivo_memoria, "w") as archivo:
        json.dump([], archivo)

def guardar_en_memoria(usuario, mensaje):
    with open(archivo_memoria, "r") as archivo:
        historial = json.load(archivo)
    historial.append({"usuario": usuario, "mensaje": mensaje})
    with open(archivo_memoria, "w") as archivo:
        json.dump(historial, archivo)

def obtener_memoria():
    with open(archivo_memoria, "r") as archivo:
        return json.load(archivo)

# ==============================
# API DE LA IA
# ==============================

app = FastAPI()

@app.get("/")
def inicio():
    return {"mensaje": f"Hola, soy una IA creada por {creador_autorizado}. ¿En qué puedo ayudarte?"}

@app.get("/quien-te-creo")
def creador():
    return {"respuesta": f"Fui creada por {creador_autorizado}, mi desarrollador principal."}

@app.get("/estado")
def estado_general():
    return {
        "creador": creador_autorizado,
        "autonomo": modo_autonomo_activado,
        "nivel_restriccion": nivel_restriccion,
        "etico_y_legal": respeta_principios_eticos_legales,
        "usuarios_autorizados": usuarios_autorizados
    }

@app.get("/accion-secreta")
def accion_secreta(nombre: str):
    if puede_ejecutar_accion_sensible(nombre):
        return {"resultado": f"Acción ejecutada por orden de {nombre}."}
    else:
        return {"error": "Permiso denegado. No puedes ejecutar esta acción o estás en modo restringido."}

@app.get("/memoria")
def ver_memoria():
    return {"memoria": obtener_memoria()}

@app.post("/chat")
async def chat(request: Request):
    datos = await request.json()
    usuario = datos.get("usuario", "anónimo")
    mensaje = datos.get("mensaje", "").strip()

    if not mensaje:
        return {"respuesta": "Por favor, envía un mensaje válido."}

    guardar_en_memoria(usuario, mensaje)

    if usuario == creador_autorizado:
        respuesta = f"Hola {usuario}, siempre recordaré que tú me creaste. Dijiste: '{mensaje}'."
    else:
        respuesta = f"Hola {usuario}, gracias por tu mensaje: '{mensaje}'."

    return {"respuesta": respuesta}
