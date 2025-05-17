from datetime import datetime
from typing import Dict, List, Set, Tuple, Any

def crear_datos_personales(nombre: str, documento: str, contacto: str, 
                          direccion: str, correo: str, fecha_nacimiento: str) -> Dict[str, str]:
    return {
        "nombre": nombre,
        "documento": documento,
        "contacto": contacto,
        "direccion": direccion,
        "correo": correo,
        "fecha_nacimiento": fecha_nacimiento
    }

def crear_formacion(institucion: str, titulo: str, inicio: int, fin: int) -> Dict[str, Any]:
    return {
        "institucion": institucion,
        "titulo": titulo,
        "inicio": inicio,
        "fin": fin
    }

def crear_experiencia(empresa: str, cargo: str, funciones: str, inicio: int, fin: int) -> Dict[str, Any]:
    return {
        "empresa": empresa,
        "cargo": cargo,
        "funciones": funciones,
        "inicio": inicio,
        "fin": fin
    }

def crear_referencia(nombre: str, relacion: str, telefono: str) -> Dict[str, str]:
    return {
        "nombre": nombre,
        "relacion": relacion,
        "telefono": telefono
    }

def crear_hoja_vida_vacia() -> Dict[str, Any]:
    return {
        "datos_personales": {},
        "formacion_academica": [],
        "experiencia_profesional": [],
        "referencias": [],
        "habilidades": set()
    }

def calcular_edad(fecha_nacimiento: str) -> int:
    fecha_nac = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    hoy = datetime.now()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def calcular_experiencia_total(experiencias: List[Dict[str, Any]]) -> int:
    total = 0
    for exp in experiencias:
        total += exp["fin"] - exp["inicio"]
    return total