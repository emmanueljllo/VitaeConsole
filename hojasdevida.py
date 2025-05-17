import json
import os
from datetime import datetime
from typing import Dict, List, Set, Any
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from modelos import (crear_datos_personales, crear_formacion, crear_experiencia, 
                    crear_referencia, crear_hoja_vida_vacia)



console = Console()

#Carga los datos desde el archivo JSON.
def cargar_datos() -> List[Dict[str, Any]]:

    if os.path.exists("datos.json"):
        try:
            with open("datos.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                # Convertir las habilidades de lista a set
                for hv in datos:
                    hv["habilidades"] = set(hv["habilidades"])
                return datos
        except Exception as e:
            console.print(f"Error al cargar datos: {e}", style="bold red")
    return []

#Guarda los datos en el archivo JSON
def guardar_datos(hojas_vida: List[Dict[str, Any]]) -> None:

    try:
        # Convierte sets a listas para serializacion JSON
        datos_serializables = []
        for hv in hojas_vida:
            hv_serializable = {
                "datos_personales": hv["datos_personales"],
                "formacion_academica": hv["formacion_academica"],
                "experiencia_profesional": hv["experiencia_profesional"],
                "referencias": hv["referencias"],
                "habilidades": list(hv["habilidades"])
            }
            datos_serializables.append(hv_serializable)
            
        with open("datos.json", "w", encoding="utf-8") as archivo:
            json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
        console.print("Datos guardados exitosamente", style="green")
    except Exception as e:
        console.print(f"Error al guardar datos: {e}", style="bold red")

#    Registra una nueva hoja de vida
def registrar_hoja_vida() -> Dict[str, Any]:
    
    console.print("\n=== Registrar Nueva Hoja de Vida ===", style="bold blue")
    try:
        hv = crear_hoja_vida_vacia()
        
        # Datos personales
        console.print("\n-- Datos Personales --", style="bold cyan")
        nombre = Prompt.ask("Nombre completo")
        documento = Prompt.ask ( " Numero de documento")
        contacto = Prompt.ask("Telefono de contacto")
        direccion = Prompt.ask("Direccion")
        correo = Prompt.ask("Correo electronico")
        fecha_nacimiento = Prompt.ask("Fecha de nacimiento (YYYY-MM-DD)")
        
        hv["datos_personales"] = crear_datos_personales(
            nombre, documento, contacto, direccion, correo, fecha_nacimiento
        )
        
        # Formacion academica
        console.print("\n-- Formacion Academica --", style="bold cyan")
        while Confirm.ask("¿Desea agregar formacion academica?"):
            institucion = Prompt.ask("Institucion educativa")
            titulo = Prompt.ask("Título obtenido")
            inicio = int(Prompt.ask("Año de inicio"))
            fin = int(Prompt.ask("Año de finalizacion"))
            
            hv["formacion_academica"].append(
                crear_formacion(institucion, titulo, inicio, fin)
            )
            
        # Experiencia profesional
        console.print("\n-- Experiencia Profesional --", style="bold cyan")
        while Confirm.ask("¿Desea agregar experiencia profesional?"):
            empresa = Prompt.ask("Empresa")
            cargo = Prompt.ask("Cargo")
            funciones = Prompt.ask("Funciones principales")
            inicio = int(Prompt.ask("Año de inicio"))
            fin = int(Prompt.ask("Año de finalizacion"))
            
            hv["experiencia_profesional"].append(
                crear_experiencia(empresa, cargo, funciones, inicio, fin)
            )
            
        # Referencias
        console.print("\n-- Referencias --", style="bold cyan")
        while Confirm.ask("¿Desea agregar una referencia?"):
            nombre = Prompt.ask("Nombre del referente")
            relacion = Prompt.ask("Relacion o cargo")
            telefono = Prompt.ask("Telefono de contacto")
            
            hv["referencias"].append(
                crear_referencia(nombre, relacion, telefono)
            )
            
        # Habilidades
        console.print("\n-- Habilidades --", style="bold cyan")
        while Confirm.ask("¿Desea agregar una habilidad?"):
            habilidad = Prompt.ask("Ingrese la habilidad")
            hv["habilidades"].add(habilidad)
            
        console.print("Hoja de vida registrada exitosamente", style="green")
        return hv
        
    except Exception as e:
        console.print(f"Error al registrar hoja de vida: {e}", style="bold red")
        return None
    
# Muestra una hoja de vida en formato legible
def mostrar_hoja_vida(hv: Dict[str, Any]) -> None:
    
    console.print("\n=== DETALLES DE HOJA DE VIDA ===", style="bold green")
    
    # Datos personales
    table = Table(title="Datos Personales")
    table.add_column("Campo", style="cyan")
    table.add_column("Valor")
    
    for campo, valor in hv["datos_personales"].items():
        table.add_row(campo.replace("_", " ").title(), valor)
        
    console.print(table)
    
    # Formacion academica
    if hv["formacion_academica"]:
        table = Table(title="Formacion Academica")
        table.add_column("Institucion")
        table.add_column("Título")
        table.add_column("Período")
        
        for formacion in hv["formacion_academica"]:
            table.add_row(
                formacion["institucion"],
                formacion["titulo"],
                f"{formacion['inicio']} - {formacion['fin']}"
            )
            
        console.print(table)
        
    # Experiencia profesional
    if hv["experiencia_profesional"]:
        table = Table(title="Experiencia Profesional")
        table.add_column("Empresa")
        table.add_column("Cargo")
        table.add_column("Funciones")
        table.add_column("Período")
        
        for exp in hv["experiencia_profesional"]:
            table.add_row(
                exp["empresa"],
                exp["cargo"],
                exp["funciones"],
                f"{exp['inicio']} - {exp['fin']}"
            )
            
        console.print(table)
        
    # Referencias
    if hv["referencias"]:
        table = Table(title="Referencias")
        table.add_column("Nombre")
        table.add_column("Relacion")
        table.add_column("Telefono")
        
        for ref in hv["referencias"]:
            table.add_row(
                ref["nombre"],
                ref["relacion"],
                ref["telefono"]
            )
            
        console.print(table)
        
    # Habilidades
    if hv["habilidades"]:
        console.print("Habilidades:", style="bold cyan")
        for hab in hv["habilidades"]:
            console.print(f"• {hab}")


#    Filtra y muestra hojas de vida 
def buscar_hoja_vida(hojas_vida: List[Dict[str, Any]]) -> None:

    if not hojas_vida:
        console.print("No hay hojas de vida registradas", style="yellow")
        return
        
    console.print("\n=== Buscar Hoja de Vida ===", style="bold blue")
    console.print("1. Por nombre")
    console.print("2. Por documento")
    console.print("3. Por correo electronico")
    console.print("4. Por años de experiencia")
    console.print("5. Por habilidad")
    
    opcion = Prompt.ask("Seleccione una opcion", choices=["1", "2", "3", "4", "5"])
    
    resultados = []
    
    if opcion == "1":
        nombre = Prompt.ask("Ingrese el nombre a buscar").lower()
        resultados = [hv for hv in hojas_vida if nombre in hv["datos_personales"].get("nombre", "").lower()]
        
    elif opcion == "2":
        documento = Prompt.ask("Ingrese el documento a buscar")
        resultados = [hv for hv in hojas_vida if documento == hv["datos_personales"].get("documento", "")]
        
    elif opcion == "3":
        correo = Prompt.ask("Ingrese el correo a buscar").lower()
        resultados = [hv for hv in hojas_vida if correo == hv["datos_personales"].get("correo", "").lower()]
        
    elif opcion == "4":
        años = int(Prompt.ask("Ingrese años mínimos de experiencia"))
        resultados = []
        for hv in hojas_vida:
            experiencia_total = sum(exp["fin"] - exp["inicio"] for exp in hv["experiencia_profesional"])
            if experiencia_total >= años:
                resultados.append(hv)
                
    elif opcion == "5":
        habilidad = Prompt.ask("Ingrese la habilidad a buscar").lower()
        resultados = [hv for hv in hojas_vida if any(habilidad in h.lower() for h in hv["habilidades"])]
    
    if resultados:
        console.print(f"Se encontraron {len(resultados)} resultados", style="green")
        for i, hv in enumerate(resultados, 1):
            console.print(f"\nResultado {i}: {hv['datos_personales'].get('nombre', 'Sin nombre')}")
            
        if len(resultados) > 0:
            indice = int(Prompt.ask("Ingrese el numero del resultado para ver detalles", default="1"))
            if 1 <= indice <= len(resultados):
                mostrar_hoja_vida(resultados[indice-1])
    else:
        console.print("\nNo se encontraron resultados", style="yellow")


#    Actualiza hoja de vida existente
def actualizar_hoja_vida(hojas_vida: List[Dict[str, Any]]) -> None:

    if not hojas_vida:
        console.print("No hay hojas de vida registradas", style="yellow")
        return
        
    console.print("\n=== Actualizar Hoja de Vida ===", style="bold blue")
    
    # Primero buscar la hoja de vida a actualizar
    documento = Prompt.ask("Ingrese el documento de la persona a actualizar")
    
    indice = None
    for i, hv in enumerate(hojas_vida):
        if hv["datos_personales"].get("documento") == documento:
            indice = i
            break
    
    if indice is None:
        console.print("\nNo se encontro ninguna hoja de vida con ese documento", style="yellow")
        return
        
    hv = hojas_vida[indice]
    mostrar_hoja_vida(hv)
    
    console.print("\nQue seccion desea actualizar?", style="bold cyan")
    console.print("1. Datos personales")
    console.print("2. Formacion academica")
    console.print("3. Experiencia profesional")
    console.print("4. Referencias")
    console.print("5. Habilidades")
    
    opcion = Prompt.ask("Seleccione una opcion", choices=["1", "2", "3", "4", "5"])
    
    if opcion == "1":
        console.print("\n-- Actualizar Datos Personales --", style="cyan")
        
        for campo in ["nombre", "contacto", "direccion", "correo"]:
            valor_actual = hv["datos_personales"].get(campo, "")
            if Confirm.ask(f"¿Desea actualizar {campo.replace('_', ' ')}? [Actual: {valor_actual}]"):
                nuevo_valor = Prompt.ask(f"Nuevo {campo.replace('_', ' ')}")
                hv["datos_personales"][campo] = nuevo_valor
                
    elif opcion == "2":
        console.print("\n-- Actualizar Formacion Academica --", style="cyan")
        console.print("1. Agregar nueva formacion")
        console.print("2. Editar formacion existente")
        console.print("3. Eliminar formacion")
        
        sub_opcion = Prompt.ask("Seleccione una opcion", choices=["1", "2", "3"])
        
        if sub_opcion == "1":
            # Agregar formacion
            institucion = Prompt.ask("Institucion educativa")
            titulo = Prompt.ask("Título obtenido")
            inicio = int(Prompt.ask("Año de inicio"))
            fin = int(Prompt.ask("Año de finalizacion"))
            
            hv["formacion_academica"].append(
                crear_formacion(institucion, titulo, inicio, fin)
            )
            
        elif sub_opcion == "2" and hv["formacion_academica"]:
            # Editar formacion
            for i, formacion in enumerate(hv["formacion_academica"], 1):
                console.print(f"{i}. {formacion['institucion']} - {formacion['titulo']}")
                
            indice_formacion = int(Prompt.ask("Seleccione la formacion a editar")) - 1
            if 0 <= indice_formacion < len(hv["formacion_academica"]):
                formacion = hv["formacion_academica"][indice_formacion]
                
                institucion = Prompt.ask("Institucion educativa", default=formacion["institucion"])
                titulo = Prompt.ask("Título obtenido", default=formacion["titulo"])
                inicio = int(Prompt.ask("Año de inicio", default=str(formacion["inicio"])))
                fin = int(Prompt.ask("Año de finalizacion", default=str(formacion["fin"])))
                
                hv["formacion_academica"][indice_formacion] = crear_formacion(
                    institucion, titulo, inicio, fin
                )
                
        elif sub_opcion == "3" and hv["formacion_academica"]:
            # Eliminar formacion
            for i, formacion in enumerate(hv["formacion_academica"], 1):
                console.print(f"{i}. {formacion['institucion']} - {formacion['titulo']}")
                
            indice_formacion = int(Prompt.ask("Seleccione la formacion a eliminar")) - 1
            if 0 <= indice_formacion < len(hv["formacion_academica"]):
                del hv["formacion_academica"][indice_formacion]
                
    elif opcion == "3":
        # Similar a la formacion academica pero con experiencia profesional
        console.print("\n-- Actualizar Experiencia Profesional --", style="cyan")
        console.print("1. Agregar nueva experiencia")
        console.print("2. Editar experiencia existente")
        console.print("3. Eliminar experiencia")
        
        sub_opcion = Prompt.ask("Seleccione una opcion", choices=["1", "2", "3"])
        
        if sub_opcion == "1":
            # Agregar experiencia
            empresa = Prompt.ask("Empresa")
            cargo = Prompt.ask("Cargo")
            funciones = Prompt.ask("Funciones principales")
            inicio = int(Prompt.ask("Año de inicio"))
            fin = int(Prompt.ask("Año de finalizacion"))
            
            hv["experiencia_profesional"].append(
                crear_experiencia(empresa, cargo, funciones, inicio, fin)
            )
            
        # Resto de logica similar a formacion academica
    elif opcion == "4":
        # Similar a formacion pero para referencias
        console.print("\n-- Actualizar Referencias --", style="cyan")
        console.print("1. Agregar nueva referencia")
        console.print("2. Editar referencia existente")
        console.print("3. Eliminar referencia")
        
        # Logica similar a las secciones anteriores
            
    elif opcion == "5":
        console.print("\n-- Actualizar Habilidades --", style="cyan")
        console.print("1. Agregar habilidad")
        console.print("2. Eliminar habilidad")
        
        sub_opcion = Prompt.ask("Seleccione una opcion", choices=["1", "2"])
        
        if sub_opcion == "1":
            habilidad = Prompt.ask("Ingrese la nueva habilidad")
            hv["habilidades"].add(habilidad)
            
        elif sub_opcion == "2" and hv["habilidades"]:
            habilidades = list(hv["habilidades"])
            for i, hab in enumerate(habilidades, 1):
                console.print(f"{i}. {hab}")
                
            indice_hab = int(Prompt.ask("Seleccione la habilidad a eliminar")) - 1
            if 0 <= indice_hab < len(habilidades):
                hv["habilidades"].remove(habilidades[indice_hab])
    
    console.print("Hoja de vida actualizada exitosamente", style="green")