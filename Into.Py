import asyncio
import random
import time

# VARIABLES DE CONFIGURACIÓN
ruta_documentos = "./documentos_sst"  # Ruta donde se almacenan los documentos
lista_documentos = ["certificado_sst.pdf", "evaluacion_riesgos.pdf", "plan_emergencias.pdf"]  # Lista de archivos a cargar

# VARIABLES DE ESTADO
documentos_cargados = []  # Documentos subidos exitosamente
documentos_pendientes = []  # Documentos que fallaron en la carga
estado_conexion = False  # Estado de conexión a internet

# VARIABLES DE CONTROL
intentos_fallidos = 0  # Contador de intentos de carga fallidos
tiempo_inicio = time.time()  # Marca de tiempo inicial

def comprobar_conexion():
    """Simula la verificación de conexión a internet."""
    global estado_conexion
    estado_conexion = random.choice([True, False])
    return estado_conexion

async def cargar_documento(nombre_archivo):
    """Función asincrónica para cargar documentos."""
    global intentos_fallidos
    print(f"Intentando cargar: {nombre_archivo}")
    await asyncio.sleep(2)  # Simula el tiempo de carga
    if comprobar_conexion():
        print(f"Documento '{nombre_archivo}' cargado exitosamente.")
        documentos_cargados.append(nombre_archivo)
    else:
        print(f" No hay conexión. Guardando '{nombre_archivo}' para carga posterior.")
        documentos_pendientes.append(nombre_archivo)
        intentos_fallidos += 1

async def procesar_carga_documentos():
    """Procesa la carga de múltiples documentos."""
    for doc in lista_documentos:
        await cargar_documento(doc)

async def reintentar_pendientes():
    """Reintenta la carga de documentos pendientes cuando hay conexión."""
    global intentos_fallidos
    while documentos_pendientes:
        print("Reintentando documentos pendientes...")
        for doc in documentos_pendientes[:]:  # Iterar sobre una copia de la lista
            if comprobar_conexion():
                print(f" Documento '{doc}' finalmente cargado.")
                documentos_cargados.append(doc)
                documentos_pendientes.remove(doc)
            else:
                print(f" Aún sin conexión para '{doc}'. Se intentará nuevamente.")
                intentos_fallidos += 1
        time.sleep(3)  # Espera antes de volver a intentar

def verificar_carga():
    """Evalúa el porcentaje de documentos cargados exitosamente."""
    total_documentos = len(lista_documentos)
    documentos_correctos = len(documentos_cargados)
    porcentaje = (documentos_correctos / total_documentos) * 100 if total_documentos > 0 else 0
    tiempo_fin = time.time()  # Marca de tiempo final
    tiempo_total = tiempo_fin - tiempo_inicio
    return (f"  Porcentaje de documentos cargados correctamente: {porcentaje:.2f}%\n"
            f"  Intentos fallidos de carga: {intentos_fallidos}\n"
            f"  Tiempo total de ejecución: {tiempo_total:.2f} segundos")

async def main():
    """Función principal que simula el flujo de carga de documentos."""
    await procesar_carga_documentos()
    await reintentar_pendientes()
    resultado = verificar_carga()
    print(resultado)