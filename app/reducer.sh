#!/bin/bash
# Reducer script para Hadoop Streaming Word Count
# Acumula las frecuencias de claves consecutivas idénticas

current_key=""
current_count=0

while IFS=$'\t' read -r key count; do
    # Si la clave es igual a la anterior, sumamos el contador
    if [ "$key" = "$current_key" ]; then
        current_count=$((current_count + count))
    else
        # Si cambia la clave y ya teníamos una previa, emitimos el resultado
        if [ -n "$current_key" ]; then
            echo -e "$current_key\t$current_count"
        fi
        current_key="$key"
        current_count=$count
    fi
done

# Emitir la última clave acumulada
if [ -n "$current_key" ]; then
    echo -e "$current_key\t$current_count"
fi
