from fastapi import APIRouter, HTTPException
from models.tarea import (
    TareaEntrada,
    TareaActualizacion,
    TareaSalida
)

from data.db import tareas_db
from datetime import datetime

router = APIRouter()

@router.post("/tareas", response_model=TareaSalida)
def crear_tarea(tarea: TareaEntrada):

    nueva_tarea = {
        "id": len(tareas_db) + 1,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad": tarea.prioridad,
        "completada": False,
        "creada_en": datetime.now(),
        "completada_en": None,
        "fecha_limite": tarea.fecha_limite
    }

    tareas_db.append(nueva_tarea)

    return nueva_tarea

@router.get("/tareas")
def listar_tareas():
    return tareas_db

@router.get("/tareas/estadisticas")
def estadisticas():

    total = len(tareas_db)

    completadas = len([
        t for t in tareas_db
        if t["completada"]
    ])

    pendientes = total - completadas

    prioridades = {
        "alta": 0,
        "media": 0,
        "baja": 0
    }

    for tarea in tareas_db:
        prioridades[tarea["prioridad"]] += 1

    return {
        "total": total,
        "completadas": completadas,
        "pendientes": pendientes,
        "por_prioridad": prioridades
    }

@router.get("/tareas/{id}")
def obtener_tarea(id: int):

    for tarea in tareas_db:
        if tarea["id"] == id:
            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )

@router.delete("/tareas/{id}")
def eliminar_tarea(id: int):

    for tarea in tareas_db:
        if tarea["id"] == id:
            tareas_db.remove(tarea)

            return {
                "mensaje": "Tarea eliminada"
            }

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )

@router.patch("/tareas/{id}")
def actualizar_tarea(
    id: int,
    datos: TareaActualizacion
):

    for tarea in tareas_db:

        if tarea["id"] == id:

            datos_actualizados = datos.model_dump(exclude_unset=True)

            for clave, valor in datos_actualizados.items():
                tarea[clave] = valor

            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )

@router.post("/tareas/{id}/completar")
def completar_tarea(id: int):

    for tarea in tareas_db:

        if tarea["id"] == id:

            tarea["completada"] = True
            tarea["completada_en"] = datetime.now()

            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )



