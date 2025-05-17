from datetime import datetime
from typing import Dict, List, Any, Tuple
from rich.console import Console
from rich.table import Table

console = Console()

#Valida que el correo tenga un formato correcto
def validar_correo(correo: str) -> bool:
   
    return "@" in correo and "." in correo.split("@")[1]


#    Valida que la fecha tenga el formato YYYY-MM-DD.
def validar_fecha(fecha: str) -> bool:

    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

#Crea un identificador único para una hoja de vida.
def crear_identificador_unico(hv: Dict[str, Any]) -> Tuple[str, str]:

    documento = hv["datos_personales"].get("documento", "")
    fecha_nacimiento = hv["datos_personales"].get("fecha_nacimiento", "")
    return (documento, fecha_nacimiento)

def mostrar_estadisticas_sistema(hojas_vida: List[Dict[str, Any]]) -> None:

    if not hojas_vida:
        console.print("\n   No hay hojas de vida registradas", style="yellow")
        return
        
    console.print("\n=== Estadísticas del Sistema ===", style="bold blue")
    
    # Conteo general
    total_hv = len(hojas_vida)
    total_experiencias = sum(len(hv["experiencia_profesional"]) for hv in hojas_vida)
    total_formaciones = sum(len(hv["formacion_academica"]) for hv in hojas_vida)
    
    # Habilidades únicas
    todas_habilidades = set()
    for hv in hojas_vida:
        todas_habilidades.update(hv["habilidades"])
    
    # Crear tabla
    table = Table(title="Estadísticas Generales")
    table.add_column("Métrica", style="cyan")
    table.add_column("Valor")
    
    table.add_row("Total hojas de vida", str(total_hv))
    table.add_row("Total experiencias registradas", str(total_experiencias))
    table.add_row("Total formaciones registradas", str(total_formaciones))
    table.add_row("Promedio experiencias por persona", f"{total_experiencias/total_hv:.2f}")
    table.add_row("Promedio formaciones por persona", f"{total_formaciones/total_hv:.2f}")
    table.add_row("Habilidades únicas registradas", str(len(todas_habilidades)))
    
    console.print(table)

def resumen_hoja_vida(hv: Dict[str, Any]) -> str:

    nombre = hv["datos_personales"].get("nombre", "Sin nombre")
    experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
    ultima_formacion = "Sin formación"
    
    if hv["formacion_academica"]:
        ultima = max(hv["formacion_academica"], key=lambda x: x["fin"])
        ultima_formacion = f"{ultima['titulo']} ({ultima['institucion']})"
    
    habilidades = ", ".join(list(hv["habilidades"])[:3])
    if len(hv["habilidades"]) > 3:
        habilidades += "..."
        
    return f"{nombre} | Exp: {experiencia_total} años | {ultima_formacion} | {habilidades}"