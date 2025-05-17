from hojasdevida import cargar_datos, guardar_datos, registrar_hoja_vida, actualizar_hoja_vida, buscar_hoja_vida
from reportes import generar_reporte, exportar_datos
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

def mostrar_menu():
    console = Console()
    console.print(Panel.fit("VitaeConsole - Sistema de gestion de hojas de vida", style="bold blue"))
    console.print("\n1. Registrar nueva hoja de vida")
    console.print("2. Buscar hoja de vida")
    console.print("3. Actualizar hoja de vida")
    console.print("4. Generar reportes")
    console.print("5. Exportar datos")
    console.print("6. Salir")
    return Prompt.ask("\nSeleccione una opcion", choices=["1", "2", "3", "4", "5", "6"])

def main():
    hojas_vida = cargar_datos()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            nueva_hv = registrar_hoja_vida()
            if nueva_hv:
                hojas_vida.append(nueva_hv)
                guardar_datos(hojas_vida)
        
        elif opcion == "2":
            buscar_hoja_vida(hojas_vida)
        
        elif opcion == "3":
            actualizar_hoja_vida(hojas_vida)
            guardar_datos(hojas_vida)
        
        elif opcion == "4":
            generar_reporte(hojas_vida)
        
        elif opcion == "5":
            exportar_datos(hojas_vida)
        
        elif opcion == "6":
            break

main()