import webbrowser
from duckduckgo_search import DDGS
from rich import print
import time
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def buscar_links(consulta, max_intentos=3):
    for intento in range(max_intentos):
        try:
            resultados = []
            with DDGS() as ddgs:
                for r in ddgs.text(consulta, max_results=10):
                    if "href" in r:
                        resultados.append(r["href"])
                    elif "url" in r:
                        resultados.append(r["url"])
            return resultados
        except Exception as e:
            if intento < max_intentos - 1:
                console.print(f"[yellow]⚠️ Intento {intento + 1} fallido. Reintentando...[/]")
                time.sleep(2)  # Esperar antes de reintentar
            else:
                console.print(f"[red]❌ Error al buscar: {str(e)}[/]")
                return []

def mostrar_links(links):
    if not links:
        console.print("[red]❌ No se encontraron enlaces.[/]")
        return
    
    console.print("\n[bold green]Resultados encontrados:[/]")
    for i, link in enumerate(links, start=1):
        console.print(f"[bold cyan]{i}[/]: {link}")

def abrir_link(links):
    if not links:
        return
        
    while True:
        try:
            opcion = Prompt.ask("\n[?] ¿Qué enlace quieres abrir?", choices=[str(i) for i in range(len(links) + 1)])
            opcion = int(opcion)
            
            if opcion == 0:
                return
                
            if 1 <= opcion <= len(links):
                webbrowser.open(links[opcion - 1])
                console.print("[green]✔ Enlace abierto en el navegador.[/]")
                return
            else:
                console.print("[red]❌ Número de enlace inválido.[/]")
        except ValueError:
            console.print("[red]❌ Por favor, ingresa un número válido.[/]")

def main():
    console.print("[bold green]🔍 Buscador de enlaces[/]")
    console.print("[dim]Escribe 'salir' para terminar[/]")
    
    while True:
        consulta = Prompt.ask("\n🔎 Ingresa lo que quieres buscar")
        
        if consulta.lower() == "salir":
            break
            
        if not consulta.strip():
            console.print("[yellow]⚠️ Por favor, ingresa un término de búsqueda.[/]")
            continue
            
        console.print("[dim]Buscando...[/]")
        links = buscar_links(consulta)
        mostrar_links(links)
        abrir_link(links)

if __name__ == "__main__":
    main()
