import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from tabulate import tabulate

console = Console()

#Genera reportes de las hojas de vida
def generar_reporte(hojas_vida: List[Dict[str, Any]]) -> None:
 
    if not hojas_vida:
        console.print("\n   No hay hojas de vida registradas para generar reportes", style="yellow")
        return
        
    console.print("\n=== Generar Reportes ===", style="bold blue")
    console.print("1. Listado de hojas de vida con experiencia superior a 'X' años")
    console.print("2. Candidatos con cierta certificacion o formacion especifica")
    console.print("3. Habilidades mas comunes")
    console.print("4. Resumen general de todas las hojas de vida")
    
    opcion = Prompt.ask("\n     Seleccione una opcion", choices=["1", "2", "3", "4"])
    
    if opcion == "1":
        años = int(Prompt.ask("Ingrese cantidad minima de años de experiencia"))
        
        table = Table(title=f"Hojas de Vida con {años}+ años de experiencia")
        table.add_column("Nombre")
        table.add_column("Documento")
        table.add_column("Años de experiencia")
        table.add_column("Experiencia mas reciente")
        
        resultados = []
        for hv in hojas_vida:
            experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
            if experiencia_total >= años:

                # Encontrar experiencia mas reciente
                exp_reciente = None
                año_max = 0
                for exp in hv["experiencia_profesional"]:
                    if exp["fin"] > año_max:
                        año_max = exp["fin"]
                        exp_reciente = exp
                
                exp_texto = f"{exp_reciente['empresa']} - {exp_reciente['cargo']}" if exp_reciente else "N/A"
                
                table.add_row(
                    hv["datos_personales"].get("nombre", ""),
                    hv["datos_personales"].get("documento", ""),
                    str(experiencia_total),
                    exp_texto
                )
                resultados.append(hv)
                
        if resultados:
            console.print(table)
        else:
            console.print(f"\n  No se encontraron hojas de vida con {años}+ años de experiencia", style="yellow")
            
    elif opcion == "2":
        formacion = Prompt.ask("Ingrese titulo o certificacion a buscar").lower()
        
        table = Table(title=f"Candidatos con formacion en '{formacion}'")
        table.add_column("Nombre")
        table.add_column("Documento")
        table.add_column("Institucion")
        table.add_column("Año")
        
        resultados = []
        for hv in hojas_vida:
            for form in hv["formacion_academica"]:
                if formacion in form["titulo"].lower():
                    table.add_row(
                        hv["datos_personales"].get("nombre", ""),
                        hv["datos_personales"].get("documento", ""),
                        form["institucion"],
                        str(form["fin"])
                    )
                    resultados.append(hv)
                    break
                
        if resultados:
            console.print(table)
        else:
            console.print(f"\n  No se encontraron candidatos con formacion en '{formacion}'", style="yellow")
            
    elif opcion == "3":
        # Habilidades mas comunes
        todas_habilidades = []
        for hv in hojas_vida:
            todas_habilidades.extend(hv["habilidades"])
            
        contador = Counter(todas_habilidades)
        habilidades_comunes = contador.most_common(10)
        
        table = Table(title="Habilidades mas comunes")
        table.add_column("Habilidad")
        table.add_column("Frecuencia")
        
        for habilidad, frecuencia in habilidades_comunes:
            table.add_row(habilidad, str(frecuencia))
            
        console.print(table)
        
    elif opcion == "4":
        # Resumen general
        table = Table(title="Resumen General de Hojas de Vida")
        table.add_column("Nombre")
        table.add_column("Experiencia")
        table.add_column("Formacion")
        table.add_column("Habilidades")
        
        for hv in hojas_vida:
            experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
            formacion = ", ".join(f.get("titulo", "") for f in hv["formacion_academica"][:2])
            habilidades = ", ".join(list(hv["habilidades"])[:3])
            
            if len(hv["habilidades"]) > 3:
                habilidades += "..."
                
            table.add_row(
                hv["datos_personales"].get("nombre", ""),
                f"{experiencia_total} años",
                formacion,
                habilidades
            )
            
        console.print(table)

#Exporta datos de hojas de vida a diferentes formatos.
def exportar_datos(hojas_vida: List[Dict[str, Any]]) -> None:
    """
    
    Args:
        hojas_vida: Lista de diccionarios con hojas de vida
    """
    if not hojas_vida:
        console.print("\n   No hay hojas de vida registradas para exportar", style="yellow")
        return
        
    console.print("\n=== Exportar Datos ===", style="bold blue")
    console.print("1. Exportar a JSON")
    console.print("2. Exportar a CSV")
    console.print("3. Exportar a TXT")
    
    opcion = Prompt.ask("Seleccione una opción", choices=["1", "2", "3"])
    
    # Preguntar si se desea exportar todas o filtrar
    todas = Confirm.ask("¿Desea exportar todas las hojas de vida?", default=True)
    
    hojas_a_exportar = hojas_vida
    
    if not todas:
        # Filtrar por algún criterio
        console.print("Filtrar por:")
        console.print("1. Años de experiencia")
        console.print("2. Formación específica")
        filtro = Prompt.ask("Seleccione una opción", choices=["1", "2"])
        
        if filtro == "1":
            años = int(Prompt.ask("Ingrese cantidad mínima de años de experiencia"))
            hojas_a_exportar = []
            for hv in hojas_vida:
                experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
                if experiencia_total >= años:
                    hojas_a_exportar.append(hv)
                    
        elif filtro == "2":
            formacion = Prompt.ask("Ingrese título o certificación a buscar").lower()
            hojas_a_exportar = []
            for hv in hojas_vida:
                for form in hv["formacion_academica"]:
                    if formacion in form["titulo"].lower():
                        hojas_a_exportar.append(hv)
                        break
    
    if not hojas_a_exportar:
        console.print("\n   No hay datos que cumplan con los criterios para exportar", style="yellow")
        return
        
    # Nombre del archivo
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_base = Prompt.ask("Nombre base del archivo", default=f"export_{fecha_actual}")
    
    if opcion == "1":
        # Exportar a JSON
        nombre_archivo = f"{nombre_base}.json"
        try:
            # Convertir sets a listas para serialización JSON
            datos_serializables = []
            for hv in hojas_a_exportar:
                hv_serializable = {
                    "datos_personales": hv["datos_personales"],
                    "formacion_academica": hv["formacion_academica"],
                    "experiencia_profesional": hv["experiencia_profesional"],
                    "referencias": hv["referencias"],
                    "habilidades": list(hv["habilidades"])
                }
                datos_serializables.append(hv_serializable)
                
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
            console.print(f"\n  Datos exportados a {nombre_archivo}", style="green")
            
        except Exception as e:
            console.print(f"\n  Error al exportar a JSON: {e}", style="bold red")
            
    elif opcion == "2":
        # Exportar a CSV
        nombre_archivo = f"{nombre_base}.csv"
        try:
            with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                
                # Encabezados
                encabezados = ["Nombre", "Documento", "Contacto", "Correo", 
                              "Experiencia Total", "Formación", "Habilidades"]
                writer.writerow(encabezados)
                
                # Datos
                for hv in hojas_a_exportar:
                    experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
                    formacion = "; ".join(f"{f['titulo']} ({f['institucion']})" for f in hv["formacion_academica"])
                    habilidades = "; ".join(hv["habilidades"])
                    
                    fila = [
                        hv["datos_personales"].get("nombre", ""),
                        hv["datos_personales"].get("documento", ""),
                        hv["datos_personales"].get("contacto", ""),
                        hv["datos_personales"].get("correo", ""),
                        str(experiencia_total),
                        formacion,
                        habilidades
                    ]
                    writer.writerow(fila)
                    
            console.print(f"\n  Datos exportados a {nombre_archivo}", style="green")
            
        except Exception as e:
            console.print(f"\n  Error al exportar a CSV: {e}", style="bold red")
            
    elif opcion == "3":
        # Exportar a TXT
        nombre_archivo = f"{nombre_base}.txt"
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as archivo:
                archivo.write("=== REPORTE DE HOJAS DE VIDA ===\n")
                archivo.write(f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for i, hv in enumerate(hojas_a_exportar, 1):
                    archivo.write(f"--- Hoja de Vida #{i} ---\n")
                    
                    # Datos personales
                    archivo.write("DATOS PERSONALES:\n")
                    for campo, valor in hv["datos_personales"].items():
                        archivo.write(f"  {campo.replace('_', ' ').title()}: {valor}\n")
                    
                    # Formación
                    if hv["formacion_academica"]:
                        archivo.write("\nFORMACIÓN ACADÉMICA:\n")
                        for form in hv["formacion_academica"]:
                            archivo.write(f"  - {form['titulo']} en {form['institucion']} ({form['inicio']}-{form['fin']})\n")
                    
                    # Experiencia
                    if hv["experiencia_profesional"]:
                        archivo.write("\nEXPERIENCIA PROFESIONAL:\n")
                        for exp in hv["experiencia_profesional"]:
                            archivo.write(f"  - {exp['cargo']} en {exp['empresa']} ({exp['inicio']}-{exp['fin']})\n")
                            archivo.write(f"    Funciones: {exp['funciones']}\n")
                    
                    # Referencias
                    if hv["referencias"]:
                        archivo.write("\nREFERENCIAS:\n")
                        for ref in hv["referencias"]:
                            archivo.write(f"  - {ref['nombre']} ({ref['relacion']}): {ref['telefono']}\n")
                    
                    # Habilidades
                    if hv["habilidades"]:
                        archivo.write("\nHABILIDADES:\n")
                        for hab in hv["habilidades"]:
                            archivo.write(f"  - {hab}\n")
                    
                    archivo.write("\n" + "="*50 + "\n\n")
                    
            console.print(f"\n  Datos exportados a {nombre_archivo}", style="green")
            
        except Exception as e:
            console.print(f"\n  Error al exportar a TXT: {e}", style="bold red")