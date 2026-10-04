"""
Script de automatización y validación funcional para Clúster Apache Hadoop HDFS / MapReduce
Universidad del Valle - Asignatura: Tecnologías Emergentes / Big Data (LG14)
Grupo 4: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez
"""

import subprocess
import time
import sys
import os

def run_cmd(cmd: str, desc: str):
    print(f"\n========================================================")
    print(f"[*] EJECUTANDO: {desc}")
    print(f"[*] COMANDO: {cmd}")
    print(f"========================================================")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print("[STDOUT]\n" + result.stdout.strip())
    if result.stderr:
        print("[STDERR]\n" + result.stderr.strip())
    if result.returncode != 0:
        print(f"[!] Advertencia: El comando finalizó con código {result.returncode}")
    else:
        print("[+] Éxito!")
    return result

def main():
    print("====================================================================")
    print("   INICIANDO PRUEBA DE CIRCUITO BIG DATA (LG14) - APACHE HADOOP     ")
    print("   Repositorio: bigdata-grupo-4                                      ")
    print("   Integrantes: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez     ")
    print("====================================================================")

    # 1. Verificar contenedores
    run_cmd("docker ps", "Paso 1: Verificación del estado de los contenedores activos")

    # 2. Creación de directorio en HDFS
    run_cmd("docker exec namenode hdfs dfs -mkdir -p /user/laboratorio", 
            "Paso 2: Crear directorio distribuido /user/laboratorio en HDFS")

    # 3. Comprobación del directorio creado
    run_cmd("docker exec namenode hdfs dfs -ls /user", 
            "Paso 3: Listar el contenido del namespace en /user")

    # 4. Creación y carga de archivo de prueba con nombres de los integrantes
    cmd_file = 'docker exec namenode bash -c "echo \'Sistemas Distribuidos Big Data - Saavedra, Linaja, Gutierrez (Grupo 4)\' > /tmp/prueba_hdfs.txt"'
    run_cmd(cmd_file, "Paso 4: Generar archivo local /tmp/prueba_hdfs.txt en NameNode")

    # 5. Cargar a HDFS
    run_cmd("docker exec namenode hdfs dfs -put -f /tmp/prueba_hdfs.txt /user/laboratorio/", 
            "Paso 5: Subir archivo a /user/laboratorio/prueba_hdfs.txt en el sistema HDFS")

    # 6. Consultar archivo almacenado por consola
    run_cmd("docker exec namenode hdfs dfs -ls /user/laboratorio", 
            "Paso 6: Listar metadatos del archivo en /user/laboratorio")

    run_cmd("docker exec namenode hdfs dfs -cat /user/laboratorio/prueba_hdfs.txt", 
            "Paso 7: Leer contenido persistido en HDFS (-cat)")

    # 7. Prueba adicional de MapReduce con Hadoop Streaming
    print("\n--------------------------------------------------------------------")
    print("   EJECUTANDO PROCESAMIENTO DISTRIBUIDO MAPREDUCE (WORD COUNT)       ")
    print("--------------------------------------------------------------------")
    
    # Asegurar permisos de ejecución en scripts
    run_cmd('docker exec namenode bash -c "chmod +x /app/mapper.sh /app/reducer.sh"', 
            "Configurar permisos de ejecución en mapper.sh y reducer.sh")

    # Crear dataset de entrada para MapReduce
    mr_input_cmd = 'docker exec namenode bash -c "hdfs dfs -mkdir -p /input_mr && echo -e \'hadoop bigdata distributed hdfs\\nhadoop mapreduce bigdata\\nhdfs cluster saavedra linaja gutierrez grupo4\' | hdfs dfs -put -f - /input_mr/data.txt"'
    run_cmd(mr_input_cmd, "Crear dataset distribuido en /input_mr/data.txt en HDFS")

    # Limpiar salida previa si existe
    run_cmd("docker exec namenode hdfs dfs -rm -r -f /output_mr", "Limpiar directorio de salida /output_mr previo")

    # Ejecutar Hadoop Streaming MapReduce
    mr_exec_cmd = (
        'docker exec namenode hadoop jar '
        '/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar '
        '-files /app/mapper.sh,/app/reducer.sh '
        '-input /input_mr/data.txt '
        '-output /output_mr '
        '-mapper mapper.sh '
        '-reducer reducer.sh'
    )
    run_cmd(mr_exec_cmd, "Ejecutar Hadoop Streaming MapReduce Job sobre YARN")

    # Ver resultados de MapReduce
    run_cmd("docker exec namenode hdfs dfs -cat /output_mr/part-00000", 
            "Consultar resultados agregados del MapReduce (/output_mr/part-00000)")

    print("\n====================================================================")
    print("   [+] CIRCUITO COMPLETO DE PRUEBAS FINALIZADO CON ÉXITO            ")
    print("   Web UI NameNode (HDFS): http://localhost:9870                    ")
    print("   Web UI YARN ResourceManager: http://localhost:8088               ")
    print("   Web UI JobHistory Server: http://localhost:8188                  ")
    print("====================================================================")

if __name__ == "__main__":
    main()
