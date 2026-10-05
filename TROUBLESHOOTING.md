# GUÍA DE RESOLUCIÓN DE PROBLEMAS Y DIAGNÓSTICO TÉCNICO (TROUBLESHOOTING)
## Laboratorio LG14: Clúster Apache Hadoop (HDFS & MapReduce) con Docker
**Asignatura:** Tecnologías Emergentes / Big Data — Universidad Privada del Valle  
**Grupo 4:** Joel Saavedra, Mauricio Linaja, Rommel Gutierrez  

---

## 1. Introducción

Durante el ciclo de vida de despliegue, configuración, persistencia y ejecución distribuida del clúster Apache Hadoop contenerizado, se presentaron diversos desafíos técnicos propios de la arquitectura de sistemas distribuidos y la interacción entre el sistema operativo host (Windows) y los contenedores Linux.

Este documento recopila de manera formal, estructurada y clara cada una de las incidencias encontradas, su causa técnica raíz, su manifestación clínica (síntomas/logs) y la solución definitiva implementada.

---

## 2. Matriz Resumen de Incidencias

| ID | Incidencia / Error Identificado | Componente Afectado | Causa Raíz | Estado de Resolución |
|---|---|---|---|---|
| **ERR-01** | `failed to connect to the docker API at npipe` | Docker Engine / Daemon | Servicio de Docker Desktop detenido en el host Windows | Resuelto |
| **ERR-02** | `InvalidAuxServiceException: The auxService:mapreduce_shuffle does not exist` | YARN (NodeManager) | Falta de declaración del ShuffleHandler en yarn-site | Resuelto |
| **ERR-03** | `mkdir: No FileSystem for scheme "C"` | CLI HDFS / Git Bash | Conversión automática de rutas POSIX a Windows en Git Bash | Resuelto |
| **ERR-04** | `Error Launching job : Output directory already exists` | MapReduce / Hadoop Streaming | Protección nativa de Hadoop contra sobreescritura de directorios | Resuelto |
| **ERR-05** | Salida con palabras repetidas no acumuladas (`bigdata 1`, `bigdata 1`) | Script Reducer (`reducer.sh`) | Falta de lógica de agregación por acumulación de claves consecutivas | Resuelto |
| **ERR-06** | `[object Object]` en Web UI al presionar *Head the file* | WebHDFS / Navegador Host | Redirección HTTP 307 al hostname interno no resuelto `datanode` | Resuelto / Explicado |
| **ERR-07** | `Conflict. The container name "/namenode" is already in use` | Docker Compose | Contenedores previos ocupando el namespace de nombres | Resuelto |

---

## 3. Análisis Detallado de Errores y Soluciones

### 3.1 Incidencia ERR-01: Fallo de Conexión con el Daemon de Docker
* **Síntoma / Mensaje de Error:**
  ```text
  failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine; 
  The system cannot find the file specified.
  ```
* **Causa Técnica:**  
  El motor de contenedores Docker Desktop no se encontraba en ejecución en el sistema anfitrión o aún estaba inicializando los sockets de comunicación inter-proceso (*Named Pipes*) con el subsistema WSL2.
* **Solución Implementada:**  
  Iniciar la aplicación Docker Desktop en Windows y validar que el estado del motor figure en verde (*Engine Running*) antes de lanzar `docker compose up -d`.

---

### 3.2 Incidencia ERR-02: Excepción de Servicio Auxiliar en YARN (Shuffle Handler)
* **Síntoma / Mensaje de Error:**
  ```text
  Container launch failed for container_... : 
  org.apache.hadoop.yarn.exceptions.InvalidAuxServiceException: The auxService:mapreduce_shuffle does not exist
  Job failed as tasks failed. failedMaps:1 failedReduces:0
  ```
* **Causa Técnica:**  
  En Hadoop 3.2.1, para que los NodeManagers puedan transferir los datos intermedios generados por los Mappers hacia los Reducers (fase de *Shuffle & Sort*), YARN requiere declarar explícitamente la clase Java encargada del servicio auxiliar `mapreduce_shuffle`.
* **Solución Implementada:**  
  Se incorporaron en `docker-compose.yml` las variables de configuración de YARN en los servicios `nodemanager` y `resourcemanager`:
  ```yaml
  environment:
    - YARN_CONF_yarn_nodemanager_aux___services=mapreduce_shuffle
    - YARN_CONF_yarn_nodemanager_aux___services_mapreduce__shuffle_class=org.apache.hadoop.mapred.ShuffleHandler
  ```

---

### 3.3 Incidencia ERR-03: Conflicto de Esquema URI en Git Bash (`Scheme "C"`)
* **Síntoma / Mensaje de Error:**
  ```text
  $ docker exec -it namenode hdfs dfs -mkdir -p /user/laboratorio
  mkdir: No FileSystem for scheme "C"
  ```
* **Causa Técnica:**  
  La capa de emulación POSIX de **Git Bash (MSYS/MinGW)** en Windows intercepta automáticamente los argumentos que inician con `/` y los convierte en rutas absolutas de Windows (ej. `C:/Program Files/Git/user/laboratorio`). Al pasar este argumento al contenedor, Hadoop interpreta `C:` como un protocolo o esquema URI inexistente.
* **Solución Implementada:**  
  Se adoptó el flujo estándar de ingresar a la consola interactiva nativa de Linux dentro del contenedor:
  ```bash
  winpty docker exec -it namenode bash
  ```
  Una vez dentro de `root@namenode:/#`, los comandos `hdfs dfs` se ejecutan en su entorno POSIX puro sin interferencia del host.  
  *(Alternativa directa en Git Bash: anteponer `MSYS_NO_PATHCONV=1` al comando o usar doble barra `//user/laboratorio`).*

---

### 3.4 Incidencia ERR-04: Colisión del Directorio de Salida en MapReduce
* **Síntoma / Mensaje de Error:**
  ```text
  ERROR streaming.StreamJob: Error Launching job : 
  Output directory hdfs://namenode:9000/output_mr already exists
  Streaming Command Failed!
  ```
* **Causa Técnica:**  
  Por directriz de diseño y seguridad de datos en Apache Hadoop, el framework MapReduce exige que el directorio de salida especificado en el parámetro `-output` **no exista** al momento de iniciar la aplicación, evitando la sobreescritura destructiva de cómputos previos.
* **Solución Implementada:**  
  Incorporar como paso previo estándar la limpieza del directorio de salida en HDFS antes de disparar el trabajo:
  ```bash
  hdfs dfs -rm -r -f /output_mr
  ```

---

### 3.5 Incidencia ERR-05: Falta de Acumulación de Claves en el Reducer
* **Síntoma / Mensaje de Error:**  
  La salida de MapReduce mostraba palabras repetidas sin totalizar:
  ```text
  bigdata     1
  bigdata     1
  hadoop      1
  hadoop      1
  ```
* **Causa Técnica:**  
  Hadoop Streaming entrega al Reducer los pares ordenados línea por línea vía `stdin`. El script `reducer.sh` original no mantenía variables de estado para comparar si la clave actual era idéntica a la anterior, imprimiendo cada línea de forma aislada.
* **Solución Implementada:**  
  Se reescribió `app/reducer.sh` con un algoritmo acumulativo en Bash con control de clave previa (`current_key` y `current_count`):
  ```bash
  #!/bin/bash
  current_key=""
  current_count=0

  while IFS=$'\t' read -r key count; do
      if [ "$key" = "$current_key" ]; then
          current_count=$((current_count + count))
      else
          if [ -n "$current_key" ]; then
              echo -e "$current_key\t$current_count"
          fi
          current_key="$key"
          current_count=$count
      fi
  done

  if [ -n "$current_key" ]; then
      echo -e "$current_key\t$current_count"
  fi
  ```
  *Resultado obtenido tras la corrección:* `bigdata 2`, `hadoop 2`, `hdfs 2`.

---

### 3.6 Incidencia ERR-06: Visualización `[object Object]` en Web UI (WebHDFS Redirect)
* **Síntoma / Mensaje de Error:**  
  Al hacer clic en *Head the file (first 32K)* en la interfaz gráfica (`http://localhost:9870`), el cuadro de previsualización muestra `[object Object]` o `Couldn't preview the file`.
* **Causa Técnica:**  
  El NameNode (puerto `9870`) solo almacena metadatos. Al solicitar el contenido del archivo, emite una redirección HTTP 307 (*WebHDFS*) apuntando al hostname interno `http://datanode:9864/...`. El navegador del host Windows no puede resolver el nombre `datanode` por DNS público, fallando la petición AJAX de JavaScript.
* **Solución y Justificación de Arquitectura:**  
  La comprobación gráfica oficial en la Web UI valida la **tabla de inodos** (permisos `-rw-r--r--`, tamaño `71 B`, dueño `root`) y el **Block ID físico** (`1073741939` asignado al DataNode). La lectura del flujo de datos en crudo se realiza de forma nativa en consola mediante:
  ```bash
  hdfs dfs -cat /user/laboratorio/prueba_hdfs.txt
  ```

---

### 3.7 Incidencia ERR-07: Conflicto de Nombres de Contenedores Previos
* **Síntoma / Mensaje de Error:**
  ```text
  Error response from daemon: Conflict. 
  The container name "/namenode" is already in use by container "...".
  ```
* **Causa Técnica:**  
  Al reconstruir la arquitectura o cambiar de directorio de trabajo, los nombres fijos definidos en `container_name` colisionan con contenedores huérfanos que permanecían registrados en Docker Engine.
* **Solución Implementada:**  
  Ejecutar la eliminación forzada de los 5 contenedores previo al levantamiento del entorno:
  ```bash
  docker rm -f namenode datanode resourcemanager nodemanager historyserver
  docker compose up -d
  ```

---

## 4. Lecciones Aprendidas y Buenas Prácticas

1. **Separación de Responsabilidades:** Comprender la distinción entre el plano de control/metadatos (NameNode) y el plano de datos físicos (DataNode) evita confusiones sobre dónde reside la información y cómo se audita.
2. **Entornos Aislados:** Utilizar sesiones interactivas (`docker exec -it namenode bash`) garantiza que los comandos de Big Data se ejecuten en el sistema operativo Linux nativo para el cual fueron diseñados.
3. **Persistencia con Volúmenes:** Los volúmenes nombrados de Docker son indispensables para mantener intacto el sistema de archivos HDFS ante el ciclo de vida de los contenedores.
4. **Validación Incremental:** El uso de scripts de prueba automatizados (`scripts/run_all_tests.py`) agiliza la detección temprana de inconsistencias en el pipeline distribuido.
