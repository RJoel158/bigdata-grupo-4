"""
Script para generar el documento PDF formal de la Guía de Demostración y Defensa Oral (LG14)
Universidad del Valle - Big Data / Sistemas Distribuidos
Grupo 4: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez
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
            self.drawString(36, 762, "UNIVALLE | Big Data (LG14) - Clúster Apache Hadoop Docker (Grupo 4)")
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
        fontSize=15,
        leading=18,
        textColor=colors.white,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#E2E8F0"),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_neutral,
        spaceAfter=3
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
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1A202C")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.2,
        leading=9,
        textColor=colors.HexColor("#742A2A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
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
        fontSize=7.8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # BANNER PORTADA
    banner_data = [
        [
            Paragraph("UNIVERSIDAD PRIVADA DEL VALLE", subtitle_style),
        ],
        [
            Paragraph("GUÍA MAESTRA DE DEMOSTRACIÓN Y DEFENSA ORAL (LG14)", title_style)
        ],
        [
            Paragraph("Asignatura: Tecnologías Emergentes / Big Data &nbsp;|&nbsp; Proyecto: Clúster Apache Hadoop con Docker<br/><b>Grupo 4:</b> Joel Saavedra &nbsp;|&nbsp; Mauricio Linaja &nbsp;|&nbsp; Rommel Gutierrez", subtitle_style)
        ]
    ]
    banner_table = Table(banner_data, colWidths=[540])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 6))

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
        ('PADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(rector_table)
    story.append(Spacer(1, 6))

    # SECCIÓN 1: CRONOGRAMA
    story.append(Paragraph("⏱️ 1. Cronograma de la Presentación (7 a 10 Minutos)", h1_style))
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
            Paragraph("<b>2. Arquitectura del Clúster</b>", table_cell),
            Paragraph("2 min", table_cell_bold),
            Paragraph("Explicar los 5 contenedores, red Bridge, volúmenes de persistencia y flujo RPC.", table_cell)
        ],
        [
            Paragraph("<b>3. Demostración en Vivo</b>", table_cell),
            Paragraph("4 min", table_cell_bold),
            Paragraph("Validar <code>docker ps</code>, HDFS Web UI (localhost:9870), comandos HDFS y Job MapReduce.", table_cell)
        ],
        [
            Paragraph("<b>4. Comparativa con docker-hadoop</b>", table_cell),
            Paragraph("2 min", table_cell_bold),
            Paragraph("Defender la tabla de 11 criterios: Hadoop Streaming y agilidad vs stack tradicional.", table_cell)
        ],
        [
            Paragraph("<b>5. Conclusiones y Cierre</b>", table_cell),
            Paragraph("1 min", table_cell_bold),
            Paragraph("Presentar historial de 5 commits atómicos y responder preguntas defensivas.", table_cell)
        ],
    ]
    crono_table = Table(crono_data, colWidths=[130, 45, 365])
    crono_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg])
    ]))
    story.append(crono_table)
    story.append(Spacer(1, 6))

    # SECCIÓN 2: GUION DE ORATORIA - FASE 1 Y 2
    story.append(Paragraph("🎙️ 2. Guion de Oratoria y Acciones en Pantalla", h1_style))

    f1_box = [
        [
            Paragraph("<b>FASE 1: Introducción y Selección del Repositorio (1 Minuto)</b>", table_cell_bold)
        ],
        [
            Paragraph("🖥️ <b>Acción en Pantalla:</b> Mostrar la portada del <code>README.md</code> (Sección 1 y 2).", body_style)
        ],
        [
            Paragraph('"Buenas tardes docente y compañeros. Para la práctica LG14 seleccionamos el repositorio público <b>hadoop-hdfs-map-reduce-docker</b> de Martin Castro Alvarez.<br/>Elegimos Apache Hadoop versión 3.2.1 porque implementa el estándar industrial de Big Data para almacenamiento distribuido en HDFS y procesamiento paralelo MapReduce vía Hadoop Streaming, cumpliendo con la consigna de ser un entorno completamente contenerizado y reproducible mediante Docker Compose."', quote_style)
        ],
        [
            Paragraph("📌 <b>Punto Clave a Resaltar:</b> Cumple con ser diferente al repositorio base, utiliza Docker Compose con 5 servicios y permite pruebas funcionales de lectura, escritura y MapReduce.", body_style)
        ]
    ]
    t_f1 = Table(f1_box, colWidths=[540])
    t_f1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f1)
    story.append(Spacer(1, 5))

    f2_box = [
        [
            Paragraph("<b>FASE 2: Comprensión y Análisis de la Arquitectura (2 Minutos)</b>", table_cell_bold)
        ],
        [
            Paragraph("🖥️ <b>Acción en Pantalla:</b> Mostrar el Diagrama Mermaid de Arquitectura en el <code>README.md</code> (Sección 4).", body_style)
        ],
        [
            Paragraph('"Analizando la arquitectura técnica, nuestro clúster se compone de 5 contenedores orquestados sobre la red Bridge privada <b>hadoop-network</b>:<br/>'
                      '1. <b>namenode:</b> Nodo maestro HDFS. Expone el puerto 9870 (Web UI) y 9000 (IPC/RPC). Administra el namespace y tabla de inodos.<br/>'
                      '2. <b>datanode:</b> Nodo esclavo de almacenamiento. Guarda físicamente los bloques de datos y reporta métricas en el puerto 9864.<br/>'
                      '3. <b>resourcemanager & nodemanager:</b> Capa YARN para planificar recursos y ejecutar contenedores de cómputo Mapper y Reducer.<br/>'
                      '4. <b>historyserver:</b> Mantiene el historial de jobs y logs en el puerto 8188.<br/>'
                      '5. <b>Volúmenes Nombrados:</b> hadoop_namenode y hadoop_datanode para persistencia física en disco."', quote_style)
        ],
        [
            Paragraph("📌 <b>Punto Clave a Resaltar:</b> Los servicios se comunican mediante resolución DNS interna (<code>hdfs://namenode:9000</code>).", body_style)
        ]
    ]
    t_f2 = Table(f2_box, colWidths=[540])
    t_f2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 4),
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
            Paragraph("<b>1. Estado de los Contenedores en Terminal:</b><br/>"
                      "<code>docker ps</code> &nbsp;&rarr;&nbsp; <i>Confirmamos 5 contenedores en estado Up y puertos activos.</i>", body_style)
        ],
        [
            Paragraph("<b>2. Monitoreo y Salud de HDFS en Web UI:</b><br/>"
                      "Abrir en navegador: <code>http://localhost:9870</code> (Overview y Live DataNodes).", body_style)
        ],
        [
            Paragraph("<b>3. Prueba Funcional 1 - Creación de Directorio en HDFS:</b><br/>"
                      "<code>docker exec -it namenode hdfs dfs -mkdir -p /user/laboratorio</code><br/>"
                      "<code>docker exec -it namenode hdfs dfs -ls /user</code>", code_style)
        ],
        [
            Paragraph("<b>4. Prueba Funcional 2 - Carga de Archivo con los Nombres del Grupo:</b><br/>"
                      "<code>docker exec -it namenode bash -c \"echo 'Sistemas Distribuidos Big Data - Saavedra, Linaja, Gutierrez (Grupo 4)' > /tmp/prueba_hdfs.txt\"</code><br/>"
                      "<code>docker exec -it namenode hdfs dfs -put -f /tmp/prueba_hdfs.txt /user/laboratorio/</code>", code_style)
        ],
        [
            Paragraph("<b>5. Prueba Funcional 3 - Consulta por Consola y Web UI:</b><br/>"
                      "<code>docker exec -it namenode hdfs dfs -ls /user/laboratorio</code><br/>"
                      "<code>docker exec -it namenode hdfs dfs -cat /user/laboratorio/prueba_hdfs.txt</code><br/>"
                      "<i>Navegación Web UI:</i> Ir a <b>Utilities &gt; Browse the file system &gt; /user/laboratorio/prueba_hdfs.txt</b>.", body_style)
        ],
        [
            Paragraph("<b>6. Prueba de Procesamiento MapReduce (Hadoop Streaming):</b><br/>"
                      "<code>docker exec -it namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /app/mapper.sh,/app/reducer.sh -input /input_mr/data.txt -output /output_mr -mapper mapper.sh -reducer reducer.sh</code><br/>"
                      "<code>docker exec -it namenode hdfs dfs -cat /output_mr/part-00000</code>", code_style)
        ]
    ]
    t_f3 = Table(f3_box, colWidths=[540])
    t_f3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f3)
    story.append(Spacer(1, 5))

    f4_box = [
        [
            Paragraph("<b>FASE 4: Análisis Comparativo Completo con docker-hadoop (2 Minutos)</b>", table_cell_bold)
        ],
        [
            Paragraph("🖥️ <b>Acción en Pantalla:</b> Mostrar la Tabla Comparativa de 11 Criterios (Sección 8 del <code>README.md</code>).<br/>"
                      '"En comparación con docker-hadoop de Big Data Europe, nuestro proyecto destaca por su despliegue autocontenido sin requerir configuraciones de entorno externas complejas, facilitando el procesamiento analítico inmediato mediante scripts de Hadoop Streaming sin necesidad de compilar pesados archivos JAR en Java."', quote_style)
        ],
        [
            Paragraph("<b>FASE 5: Conclusiones y Cumplimiento de Entrega (1 Minuto)</b>", table_cell_bold)
        ],
        [
            Paragraph('🖥️ <b>Acción en Pantalla:</b> Ejecutar <code>git log --oneline</code> en terminal.<br/>'
                      '"Finalizamos demostrando el historial de 5 commits atómicos realizados en nuestro repositorio <b>bigdata-grupo-4</b>, cumpliendo con la totalidad de requisitos del documento LG14. Quedamos a disposición para preguntas."', quote_style)
        ]
    ]
    t_f4 = Table(f4_box, colWidths=[540])
    t_f4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#E2E8F0")),
    ]))
    story.append(t_f4)

    # PAGE BREAK TO PAGE 3
    story.append(PageBreak())

    # TABLA COMPARATIVA
    story.append(Paragraph("📊 3. Tabla Comparativa Exhaustiva (11 Criterios Oficiales)", h1_style))
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
        ('PADDING', (0,0), (-1,-1), 2.8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, light_bg])
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 6))

    # SECCIÓN 4: BANCO DE PREGUNTAS DEFENSIVAS
    story.append(Paragraph("🛡️ 4. Banco de Preguntas Defensivas Resueltas", h1_style))
    faq_data = [
        [
            Paragraph("<b>❓ P1: ¿Cuál es la diferencia entre el NameNode y el DataNode en HDFS?</b><br/>"
                      "<b>Respuesta:</b> El NameNode gestiona metadatos en RAM (namespace, inodos, mapeo de bloques). Los DataNodes almacenan y leen físicamente los bloques en disco.", body_style)
        ],
        [
            Paragraph("<b>❓ P2: ¿Por qué se utilizan los puertos 9870 y 9000 en el NameNode?</b><br/>"
                      "<b>Respuesta:</b> El puerto <code>9870</code> es la Web UI HTTP (Hadoop 3.x) y el <code>9000</code> es el puerto IPC/RPC binario para operaciones cliente.", body_style)
        ],
        [
            Paragraph("<b>❓ P3: ¿Qué ventaja ofrece Hadoop Streaming frente al MapReduce en Java?</b><br/>"
                      "<b>Respuesta:</b> Usa flujos estándar (<code>stdin/stdout</code>), permitiendo scripts en Python o Bash sin compilar código Java.", body_style)
        ],
        [
            Paragraph("<b>❓ P4: ¿Cómo garantiza el clúster la tolerancia a fallos y la persistencia de datos?</b><br/>"
                      "<b>Respuesta:</b> Volúmenes Docker nombrados conservan <code>fsimage</code> y bloques en el host; HDFS redistribuye réplicas si un DataNode cae.", body_style)
        ],
    ]
    t_faq = Table(faq_data, colWidths=[540])
    t_faq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_faq)
    story.append(Spacer(1, 6))

    # SECCIÓN 5: CHECKLIST
    story.append(Paragraph("📋 5. Checklist Pre-Presentación y Commits del Repositorio", h1_style))
    chk_text = (
        "&bull; <b>Docker Desktop:</b> Activo &nbsp;|&nbsp; "
        "<b>Contenedores:</b> 5 servicios en estado <code>Up</code> (<code>docker ps</code>) &nbsp;|&nbsp; "
        "<b>Web UI:</b> <code>http://localhost:9870</code><br/>"
        "&bull; <b>Terminal:</b> Directorio <code>bigdata-grupo-4</code> listo &nbsp;|&nbsp; "
        "<b>Historial:</b> 5 Commits atómicos de <code>Rjoel &lt;svr0035567@est.univalle.edu&gt;</code>."
    )
    story.append(Paragraph(chk_text, body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Documento PDF generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
