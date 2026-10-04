"""
Script para generar el documento PDF formal de la Guía de Demostración y Defensa Oral (LG14)
Universidad del Valle - Big Data / Sistemas Distribuidos
Grupo 4: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez
Estilo: Académico y formal (sin emojis), con explicación de 4 capas arquitectónicas.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "UNIVERSIDAD PRIVADA DEL VALLE | Big Data (LG14) - Clúster Apache Hadoop (Grupo 4)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(36, 754, 576, 754)
        
        # Footer
        footer_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 25, footer_text)
        self.drawString(36, 25, "Joel Saavedra | Mauricio Linaja | Rommel Gutierrez — Repositorio: bigdata-grupo-4")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)
        self.restoreState()

def build_pdf(filename="Guia_Demostracion_y_Defensa_LG14_Grupo4.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A365D")
    secondary_color = colors.HexColor("#2B6CB0")
    dark_neutral = colors.HexColor("#2D3748")
    light_bg = colors.HexColor("#F7FAFC")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=16.5,
        textColor=colors.white,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        textColor=colors.HexColor("#E2E8F0"),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=primary_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.6,
        textColor=dark_neutral,
        spaceAfter=2
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    quote_style = ParagraphStyle(
        'QuoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.4,
        leading=9.6,
        textColor=colors.HexColor("#1A202C")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=6.8,
        leading=8.2,
        textColor=colors.HexColor("#742A2A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.1,
        leading=8.8,
        textColor=dark_neutral
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#1A202C")
    )

    table_cell_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        fontSize=7.3,
        leading=9.2,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # BANNER PORTADA FORMAL
    banner_data = [
        [
            Paragraph("UNIVERSIDAD PRIVADA DEL VALLE &nbsp;|&nbsp; FACULTAD DE INGENIERÍA", subtitle_style),
        ],
        [
            Paragraph("GUÍA MAESTRA DE DEMOSTRACIÓN Y DEFENSA ORAL (LG14)", title_style)
        ],
        [
            Paragraph("Asignatura: Tecnologías Emergentes / Big Data &nbsp;|&nbsp; Proyecto: Clúster Apache Hadoop en Docker<br/><b>Grupo 4:</b> Joel Saavedra &nbsp;|&nbsp; Mauricio Linaja &nbsp;|&nbsp; Rommel Gutierrez", subtitle_style)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 4))

    # CRITERIO RECTOR
    rector_box = [
        [
            Paragraph("<b>Criterio Rector de Evaluación LG14:</b> Encontrar &rarr; Comprender &rarr; Desplegar &rarr; Probar &rarr; Analizar", bold_body)
        ]
    ]
    rector_table = Table(rector_box, colWidths=[540])
    rector_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(rector_table)
    story.append(Spacer(1, 4))

    # SECCIÓN 1: CRONOGRAMA
    story.append(Paragraph("1. Cronograma de la Presentación (7 a 10 Minutos)", h1_style))
    crono_data = [
        [
            Paragraph("Fase", table_cell_header),
            Paragraph("Tiempo", table_cell_header),
            Paragraph("Objetivo Principal de la Demostración", table_cell_header)
        ],
        [
            Paragraph("<b>1. Introducción y Selección</b>", table_cell),
            Paragraph("1 min", table_cell_bold),
            Paragraph("Justificar la elección de Apache Hadoop (HDFS/MapReduce) y registro formal del repositorio.", table_cell)
        ],
        [
            Paragraph("<b>2. Arquitectura (4 Capas)</b>", table_cell),
            Paragraph("2 min", table_cell_bold),
            Paragraph("Explicar las 4 capas: Host, HDFS (NameNode/DataNode), YARN (RM/NM/History) y Persistencia.", table_cell)
        ],
        [
            Paragraph("<b>3. Demostración en Vivo</b>", table_cell),
            Paragraph("4 min", table_cell_bold),
            Paragraph("Validar docker ps, Web UI HDFS (localhost:9870), comandos HDFS y Job MapReduce en YARN.", table_cell)
        ],
        [
            Paragraph("<b>4. Comparativa con docker-hadoop</b>", table_cell),
            Paragraph("2 min", table_cell_bold),
            Paragraph("Defender la tabla de 11 criterios: Hadoop Streaming y agilidad vs stack tradicional.", table_cell)
        ],
        [
            Paragraph("<b>5. Conclusiones y Cierre</b>", table_cell),
            Paragraph("1 min", table_cell_bold),
            Paragraph("Presentar historial de commits atómicos y responder preguntas defensivas.", table_cell)
        ],
    ]
    crono_table = Table(crono_data, colWidths=[130, 45, 365])
    crono_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg])
    ]))
    story.append(crono_table)
    story.append(Spacer(1, 4))

    # SECCIÓN 2: GUION DE ORATORIA - FASE 1 Y 2
    story.append(Paragraph("2. Guion de Oratoria y Acciones en Pantalla", h1_style))

    f1_box = [
        [
            Paragraph("<b>FASE 1: Introducción y Selección del Repositorio (1 Minuto)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Acción en Pantalla:</b> Mostrar la portada del documento README.md (Secciones 1 y 2).", body_style)
        ],
        [
            Paragraph('"Buenas tardes docente y compañeros. Para la práctica LG14 seleccionamos el repositorio público <b>hadoop-hdfs-map-reduce-docker</b> de Martin Castro Alvarez.<br/>Elegimos Apache Hadoop versión 3.2.1 porque implementa el estándar industrial de Big Data para almacenamiento distribuido en HDFS y procesamiento paralelo MapReduce vía Hadoop Streaming, cumpliendo con la consigna de ser un entorno completamente contenerizado y reproducible mediante Docker Compose."', quote_style)
        ]
    ]
    t_f1 = Table(f1_box, colWidths=[540])
    t_f1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f1)
    story.append(Spacer(1, 3.5))

    f2_box = [
        [
            Paragraph("<b>FASE 2: Exposición de la Arquitectura en 4 Capas (2 Minutos)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Acción en Pantalla:</b> Mostrar el Diagrama Mermaid de Arquitectura en el README.md (Sección 4).", body_style)
        ],
        [
            Paragraph("<b>1. Capa Superior (Host Local Windows):</b> \"Desde aquí interactuamos con el clúster a nivel de consola mediante Docker CLI ejecutando docker exec para ingresar al NameNode, y a nivel visual desde el Navegador Web en los puertos clave: 9870 (HDFS), 8088 (YARN) y 8188 (HistoryServer).\"<br/>"
                      "<b>2. Red y Capa HDFS (Almacenamiento):</b> \"Los contenedores conviven en la red Bridge privada hadoop-network. El NameNode administra el namespace e inodos en memoria y atiende en el puerto 9000; el DataNode guarda físicamente los bloques de datos y reporta heartbeats y métricas en el puerto 9864.\"<br/>"
                      "<b>3. Capa YARN (Cómputo Distribuido):</b> \"El ResourceManager coordina recursos globales, el NodeManager ejecuta los contenedores de cómputo Mapper/Reducer y el HistoryServer almacena logs de trabajos finalizados.\"<br/>"
                      "<b>4. Capa de Persistencia (Inferior):</b> \"Volúmenes nombrados hadoop_namenode, hadoop_datanode y hadoop_historyserver preservan metadatos, bloques y logs en el disco del host ante reinicios.\"<br/>"
                      "<b>Cierre de Arquitectura:</b> \"Gracias a esta arquitectura, cuando ejecutamos un hdfs dfs -put, el cliente le pide ubicación al NameNode, el archivo se transfiere y almacena en bloques dentro del DataNode, persiste en el volumen y lo auditamos en tiempo real en el puerto 9870.\"", quote_style)
        ]
    ]
    t_f2 = Table(f2_box, colWidths=[540])
    t_f2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f2)

    # PAGE BREAK TO PAGE 2
    story.append(PageBreak())

    # FASE 3, 4 Y 5
    f3_box = [
        [
            Paragraph("<b>FASE 3: Despliegue y Demostración Práctica en Vivo (4 Minutos)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Paso 1: Estado de los Contenedores en Terminal:</b><br/>"
                      "<code>docker ps</code> &nbsp;&rarr;&nbsp; <i>Confirmamos 5 contenedores en estado Up y puertos activos.</i>", body_style)
        ],
        [
            Paragraph("<b>Paso 2: Ingreso a la Consola Nativa del NameNode:</b><br/>"
                      "<code>winpty docker exec -it namenode bash</code> (Acceso directo a Linux en root@namenode:/#).", code_style)
        ],
        [
            Paragraph("<b>Paso 3: Verificación de Salud del Clúster HDFS:</b><br/>"
                      "<code>hdfs dfsadmin -report</code> &nbsp;&rarr;&nbsp; <i>Reporta Live datanodes: 1, capacidad de ~940 GB y 0 bloques corruptos.</i>", body_style)
        ],
        [
            Paragraph("<b>Paso 4: Creación de Directorio en HDFS (Requisito Obligatorio 1):</b><br/>"
                      "<code>hdfs dfs -mkdir -p /user/laboratorio</code><br/>"
                      "<code>hdfs dfs -ls /user</code> &nbsp;&rarr;&nbsp; <i>Crea la ruta distribuida en el namespace de inodos.</i>", code_style)
        ],
        [
            Paragraph("<b>Paso 5: Carga de Archivo con Integrantes (Requisito Obligatorio 2):</b><br/>"
                      "<code>echo \"Sistemas Distribuidos Big Data - Saavedra, Linaja, Gutierrez (Grupo 4)\" &gt; /tmp/prueba_hdfs.txt</code><br/>"
                      "<code>hdfs dfs -put -f /tmp/prueba_hdfs.txt /user/laboratorio/</code>", code_style)
        ],
        [
            Paragraph("<b>Paso 6: Consulta por Consola y Web UI (Requisito Obligatorio 3):</b><br/>"
                      "<code>hdfs dfs -ls /user/laboratorio</code><br/>"
                      "<code>hdfs dfs -cat /user/laboratorio/prueba_hdfs.txt</code><br/>"
                      "<i>Navegación Web UI:</i> Ir a <b>http://localhost:9870 &gt; Utilities &gt; Browse the file system &gt; /user/laboratorio/prueba_hdfs.txt</b>. Clic en <b>Head the file (first 32K)</b> para ver el contenido y auditar el <b>Block ID</b>.", body_style)
        ],
        [
            Paragraph("<b>Paso 7: Procesamiento Distribuido MapReduce con Hadoop Streaming:</b><br/>"
                      "<code>hdfs dfs -mkdir -p /input_mr &amp;&amp; echo -e \"hadoop bigdata distributed hdfs\\nhadoop mapreduce bigdata\\nhdfs cluster saavedra linaja gutierrez grupo4\" | hdfs dfs -put -f - /input_mr/data.txt</code><br/>"
                      "<code>hdfs dfs -rm -r -f /output_mr</code><br/>"
                      "<code>hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /app/mapper.sh,/app/reducer.sh -input /input_mr/data.txt -output /output_mr -mapper mapper.sh -reducer reducer.sh</code><br/>"
                      "<code>hdfs dfs -cat /output_mr/part-00000</code>", code_style)
        ]
    ]
    t_f3 = Table(f3_box, colWidths=[540])
    t_f3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f3)
    story.append(Spacer(1, 3.5))

    f4_box = [
        [
            Paragraph("<b>FASE 4: Análisis Comparativo Completo con docker-hadoop (2 Minutos)</b>", table_cell_bold)
        ],
        [
            Paragraph("<b>Acción en Pantalla:</b> Mostrar la Tabla Comparativa de 11 Criterios (Sección 8 del README.md).<br/>"
                      '"En comparación con docker-hadoop de Big Data Europe, nuestro proyecto destaca por su despliegue autocontenido sin requerir configuraciones de entorno externas complejas, facilitando el procesamiento analítico inmediato mediante scripts de Hadoop Streaming sin necesidad de compilar pesados archivos JAR en Java."', quote_style)
        ],
        [
            Paragraph("<b>FASE 5: Conclusiones y Cumplimiento de Entrega (1 Minuto)</b>", table_cell_bold)
        ],
        [
            Paragraph('<b>Acción en Pantalla:</b> Ejecutar <code>git log --oneline</code> en terminal.<br/>'
                      '"Finalizamos demostrando el historial de commits atómicos realizados en nuestro repositorio <b>bigdata-grupo-4</b>, cumpliendo con la totalidad de requisitos del documento LG14. Quedamos a disposición para preguntas."', quote_style)
        ]
    ]
    t_f4 = Table(f4_box, colWidths=[540])
    t_f4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f4)

    # PAGE BREAK TO PAGE 3
    story.append(PageBreak())

    # TABLA COMPARATIVA
    story.append(Paragraph("3. Tabla Comparativa Exhaustiva (11 Criterios Oficiales)", h1_style))
    comp_data = [
        [
            Paragraph("Criterio Oficial", table_cell_header),
            Paragraph("docker-hadoop (Referencia BDE)", table_cell_header),
            Paragraph("hadoop-hdfs-map-reduce-docker (Nuestro Proyecto)", table_cell_header)
        ],
        [
            Paragraph("<b>1. Tecnología Principal</b>", table_cell),
            Paragraph("Apache Hadoop (HDFS + YARN)", table_cell),
            Paragraph("Apache Hadoop (HDFS + MapReduce Streaming)", table_cell)
        ],
        [
            Paragraph("<b>2. Docker</b>", table_cell),
            Paragraph("Sí (Imágenes Debian GNU/Linux)", table_cell),
            Paragraph("Sí (Imágenes Debian Buster OpenJDK 8)", table_cell)
        ],
        [
            Paragraph("<b>3. Docker Compose</b>", table_cell),
            Paragraph("Sí (Formato v2/v3 con .env externo)", table_cell),
            Paragraph("Sí (Orquestación modular autocontenida)", table_cell)
        ],
        [
            Paragraph("<b>4. Contenedores</b>", table_cell),
            Paragraph("5 contenedores monolíticos", table_cell),
            Paragraph("5 contenedores especializados (NameNode, DataNode, YARN, etc.)", table_cell)
        ],
        [
            Paragraph("<b>5. Almacenamiento</b>", table_cell),
            Paragraph("HDFS multi-nodo tradicional", table_cell),
            Paragraph("HDFS modularizado con persistencia nombrada", table_cell)
        ],
        [
            Paragraph("<b>6. Procesamiento</b>", table_cell),
            Paragraph("MapReduce sobre Java clásico", table_cell),
            Paragraph("MapReduce ágil vía Hadoop Streaming (Bash/Python)", table_cell)
        ],
        [
            Paragraph("<b>7. Interfaces Web</b>", table_cell),
            Paragraph("NameNode (9870), YARN (8088), History (8188)", table_cell),
            Paragraph("NameNode Web UI (9870), YARN (8088), History (8188)", table_cell)
        ],
        [
            Paragraph("<b>8. Persistencia</b>", table_cell),
            Paragraph("Volúmenes montados en carpetas de contenedor", table_cell),
            Paragraph("Volúmenes nombrados dedicados (hadoop_namenode, hadoop_datanode)", table_cell)
        ],
        [
            Paragraph("<b>9. Complejidad Inst.</b>", table_cell),
            Paragraph("Media-Alta (dependencia estricta de archivo .env)", table_cell),
            Paragraph("Muy Baja (despliegue directo con <code>docker compose up -d</code>)", table_cell)
        ],
        [
            Paragraph("<b>10. Documentación</b>", table_cell),
            Paragraph("Genérica orientada al stack BDE", table_cell),
            Paragraph("Práctica y enfocada en pipelines MapReduce y HDFS", table_cell)
        ],
        [
            Paragraph("<b>11. Caso de Uso</b>", table_cell),
            Paragraph("Infraestructura base para conectar Hive/Spark", table_cell),
            Paragraph("Laboratorio ágil de almacenamiento masivo y algoritmos paralelos", table_cell)
        ],
    ]
    comp_table = Table(comp_data, colWidths=[110, 215, 215])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg])
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 4))

    # SECCIÓN 4: BANCO DE PREGUNTAS DEFENSIVAS
    story.append(Paragraph("4. Banco de Preguntas Defensivas Resueltas", h1_style))
    faq_data = [
        [
            Paragraph("<b>Pregunta 1: ¿Cuál es la diferencia entre el NameNode y el DataNode en HDFS?</b><br/>"
                      "<b>Respuesta:</b> El NameNode gestiona metadatos en RAM (namespace, inodos, mapeo de bloques). Los DataNodes almacenan y leen físicamente los bloques en disco.", body_style)
        ],
        [
            Paragraph("<b>Pregunta 2: ¿Por qué se utilizan los puertos 9870 y 9000 en el NameNode?</b><br/>"
                      "<b>Respuesta:</b> El puerto <code>9870</code> es la Web UI HTTP (Hadoop 3.x) y el <code>9000</code> es el puerto IPC/RPC binario para operaciones cliente.", body_style)
        ],
        [
            Paragraph("<b>Pregunta 3: ¿Qué ventaja ofrece Hadoop Streaming frente al MapReduce en Java?</b><br/>"
                      "<b>Respuesta:</b> Usa flujos estándar (<code>stdin/stdout</code>), permitiendo scripts en Python o Bash sin compilar código Java.", body_style)
        ],
        [
            Paragraph("<b>Pregunta 4: ¿Cómo garantiza el clúster la tolerancia a fallos y la persistencia de datos?</b><br/>"
                      "<b>Respuesta:</b> Volúmenes Docker nombrados conservan <code>fsimage</code> y bloques en el host; HDFS redistribuye réplicas si un DataNode cae.", body_style)
        ],
    ]
    t_faq = Table(faq_data, colWidths=[540])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 3.2),
    ]))
    story.append(t_faq)
    story.append(Spacer(1, 4))

    # SECCIÓN 5: CHECKLIST
    story.append(Paragraph("5. Checklist Pre-Presentación y Commits del Repositorio", h1_style))
    chk_text = (
        "• <b>Docker Engine:</b> Activo y operativo en segundo plano.<br/>"
        "• <b>Contenedores:</b> 5 servicios en estado Up (docker ps) | Web UI HDFS: http://localhost:9870 | YARN: http://localhost:8088<br/>"
        "• <b>Terminal:</b> Carpeta del proyecto lista para demostración interactiva en consola Linux.<br/>"
        "• <b>Historial de Commits:</b> Commits atómicos escalonados de Rjoel &lt;svr0035567@est.univalle.edu&gt;."
    )
    story.append(Paragraph(chk_text, body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Documento PDF generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
