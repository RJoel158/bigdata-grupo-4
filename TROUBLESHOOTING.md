# Guía de Resolución de Problemas (Troubleshooting)
## Clúster Apache Hadoop con Docker — Grupo 4

Este documento resume de forma clara y directa los errores técnicos encontrados durante la configuración y ejecución del clúster, su causa y la solución aplicada.

---

### 1. Fallo de Conexión con Docker (Daemon no iniciado)
* **Problema:** Al ejecutar comandos de Docker, aparece el mensaje:
  ```text
  failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
  ```
* **Causa:** La aplicación Docker Desktop estaba cerrada o su motor interno aún no había terminado de arrancar en Windows.
* **Solución:** Iniciar Docker Desktop en Windows y esperar a que el indicador esté en verde (*Engine Running*) antes de ejecutar comandos.

---

### 2. Error en YARN al ejecutar MapReduce (Shuffle Handler)
* **Problema:** El trabajo MapReduce fallaba en la etapa de mapeo con el error:
  ```text
  InvalidAuxServiceException: The auxService:mapreduce_shuffle does not exist
  ```
* **Causa:** En Apache Hadoop 3.2.1, el servicio NodeManager necesita saber explícitamente qué clase Java se encarga de transferir los datos intermedios entre Mappers y Reducers (*fase de Shuffle*).
* **Solución:** Se agregaron las siguientes variables de entorno en `docker-compose.yml` para los servicios de YARN:
  ```yaml
  - YARN_CONF_yarn_nodemanager_aux___services=mapreduce_shuffle
  - YARN_CONF_yarn_nodemanager_aux___services_mapreduce__shuffle_class=org.apache.hadoop.mapred.ShuffleHandler
  ```

---

### 3. Error por Carpeta de Salida Existente en MapReduce
* **Problema:** Al volver a lanzar el trabajo MapReduce, salía el error:
  ```text
  Output directory hdfs://namenode:9000/output_mr already exists
  ```
* **Causa:** Por seguridad, Hadoop prohíbe escribir en una carpeta de salida que ya existe para evitar sobrescribir o borrar resultados previos por accidente.
* **Solución:** Eliminar la carpeta de salida anterior en HDFS antes de ejecutar un nuevo trabajo:
  ```bash
  hdfs dfs -rm -r -f /output_mr
  ```

---

### 4. Conteo de Palabras Repetidas no Acumulado en el Reducer
* **Problema:** La salida de MapReduce mostraba palabras repetidas sin sumarlas (por ejemplo: `bigdata 1` y `bigdata 1`).
* **Causa:** El script `reducer.sh` original procesaba cada línea por separado sin mantener un acumulador de la clave anterior para sumar los valores.
* **Solución:** Se modificó `app/reducer.sh` para que acumule los valores mientras la palabra sea la misma y solo imprima el total al cambiar de palabra:
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
  *Resultado final correcto:* `bigdata 2`, `hadoop 2`, `hdfs 2`.

---

### 5. Cuadro `[object Object]` en la Web UI al previsualizar archivo
* **Problema:** Al hacer clic en *Head the file* dentro de la Web UI (`http://localhost:9870`), el cuadro muestra `[object Object]`.
* **Causa:** La Web UI pertenece al NameNode, el cual solo maneja metadatos. Al pedir el contenido, el NameNode redirige la solicitud hacia el DataNode (`http://datanode:9864`), pero el navegador en Windows no conoce el nombre interno `datanode`.
* **Solución / Explicación:** En la Web UI se demuestran los metadatos reales (permisos, tamaño de 71 bytes y el Block ID asignado al DataNode). La lectura del contenido en texto plano se valida directamente en la terminal con:
  ```bash
  hdfs dfs -cat /user/laboratorio/prueba_hdfs.txt
  ```

---

### 6. Conflicto de Nombres al Levantar Contenedores
* **Problema:** Al recrear el clúster salía:
  ```text
  Conflict. The container name "/namenode" is already in use
  ```
* **Causa:** Quedaron contenedores anteriores con el mismo nombre en ejecución o detenidos.
* **Solución:** Eliminar los contenedores anteriores antes de volver a levantar el clúster:
  ```bash
  docker rm -f namenode datanode resourcemanager nodemanager historyserver
  docker compose up -d
  ```
