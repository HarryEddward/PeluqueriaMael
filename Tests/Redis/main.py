import numpy as np
from collections import Counter
import math
import re

# Documentos de ejemplo
documentos = [
    "El desarrollo web es una habilidad importante para los programadores modernos.",
    "Python es un lenguaje de programación versátil y popular.",
    "Las bases de datos permiten almacenar y gestionar grandes volúmenes de datos.",
    "Docker facilita la creación de entornos de desarrollo consistentes.",
    "El aprendizaje automático puede mejorar la precisión de los modelos predictivos.",
    "Los microservicios permiten construir aplicaciones escalables y mantenibles.",
    "El análisis de datos ayuda a tomar decisiones basadas en evidencias.",
    "React es una biblioteca de JavaScript para construir interfaces de usuario.",
    "El manejo de errores es crucial en el desarrollo de software.",
    "SQL es un lenguaje de consulta estructurado para interactuar con bases de datos.",
    "La integración continua mejora la calidad del software al automatizar las pruebas.",
    "La normalización de datos asegura que la información sea consistente.",
    "La visualización de datos facilita la interpretación de grandes conjuntos de datos.",
    "El caching mejora el rendimiento al reducir el tiempo de acceso a datos.",
    "El versionado de código permite realizar un seguimiento de los cambios en el software.",
    "La seguridad en la web es fundamental para proteger los datos de los usuarios.",
    "La optimización de consultas mejora la eficiencia en las bases de datos.",
    "El testing automatizado ayuda a detectar errores de manera temprana.",
    "El despliegue continuo permite actualizar aplicaciones con frecuencia y sin problemas.",
    "El análisis de sentimientos puede determinar la actitud de los textos.",
    "Las API RESTful facilitan la comunicación entre aplicaciones.",
    "La arquitectura de software define la estructura de los sistemas de software.",
    "El aprendizaje profundo utiliza redes neuronales para resolver problemas complejos.",
    "El control de versiones ayuda a gestionar el desarrollo de proyectos colaborativos.",
    "La normalización en bases de datos evita redundancias y mantiene la integridad.",
    "El procesamiento del lenguaje natural permite que las máquinas entiendan el texto humano.",
    "El análisis exploratorio de datos ayuda a descubrir patrones y anomalías.",
    "El diseño responsivo asegura que las aplicaciones web se adapten a diferentes dispositivos.",
    "La programación orientada a objetos organiza el código en objetos y clases.",
    "Las pruebas unitarias aseguran que cada parte del código funcione correctamente.",
    "La computación en la nube permite acceder a recursos informáticos a través de internet.",
    "El diseño de base de datos relacional organiza la información en tablas relacionadas.",
    "La recuperación de información mejora la relevancia de los resultados de búsqueda.",
    "El análisis de redes sociales proporciona información sobre la interacción de los usuarios.",
    "El uso de contenedores facilita la portabilidad de las aplicaciones.",
    "La escalabilidad es importante para manejar el crecimiento de las aplicaciones.",
    "El análisis de series temporales ayuda a prever futuros eventos basados en datos históricos.",
    "La autenticación de usuarios protege las aplicaciones contra accesos no autorizados.",
    "La normalización de textos mejora la calidad de los análisis lingüísticos.",
    "La configuración de entornos de desarrollo es clave para mantener la consistencia en el equipo.",
    "El uso de frameworks acelera el desarrollo al proporcionar herramientas predefinidas.",
    "La integración de sistemas permite que diferentes aplicaciones trabajen juntas.",
    "El análisis predictivo utiliza datos para hacer predicciones sobre eventos futuros.",
    "La depuración es esencial para identificar y corregir errores en el código.",
    "La gestión de sesiones en aplicaciones web mantiene el estado del usuario.",
    "El diseño de UI/UX se enfoca en la experiencia del usuario en las aplicaciones.",
    "El análisis de clústeres agrupa datos similares para simplificar su interpretación.",
    "La administración de redes asegura la comunicación eficiente entre sistemas.",
    "El análisis de frecuencia de palabras ayuda a entender los temas principales de un texto.",
    "El uso de patrones de diseño mejora la estructura del código y su mantenibilidad.",
    "El procesamiento de imágenes utiliza algoritmos para mejorar y analizar fotos y videos.",
    "El aprendizaje automático supervisado utiliza datos etiquetados para entrenar modelos.",
    "El análisis de datos en tiempo real permite tomar decisiones basadas en la información actual.",
    "La optimización de rendimiento asegura que las aplicaciones funcionen de manera eficiente.",
    "La automatización de tareas repetitivas reduce el tiempo y esfuerzo manual.",
    "La integración de APIs permite extender la funcionalidad de las aplicaciones.",
    "El análisis de sentimientos en redes sociales proporciona información sobre la percepción pública.",
    "La implementación de seguridad en aplicaciones web previene ataques y vulnerabilidades.",
    "El diseño modular facilita la actualización y mantenimiento de las aplicaciones.",
    "La gestión de versiones de base de datos ayuda a mantener el historial de cambios.",
    "El análisis de datos cualitativos proporciona una comprensión más profunda de los datos no numéricos.",
    "La optimización de algoritmos mejora la velocidad y eficiencia de los procesos computacionales.",
    "La programación funcional utiliza funciones puras para desarrollar software.",
    "El uso de métodos de agrupamiento ayuda a encontrar patrones en grandes conjuntos de datos.",
    "La planificación de capacidad asegura que los recursos sean suficientes para manejar la carga.",
    "El análisis de datos de clientes ayuda a personalizar las ofertas y mejorar la satisfacción.",
    "La implementación de técnicas de machine learning mejora la precisión de los modelos.",
    "El análisis de tendencias proporciona información sobre cambios en los datos a lo largo del tiempo.",
    "La gestión de riesgos en proyectos de TI identifica y mitiga problemas potenciales.",
    "La arquitectura de microservicios divide aplicaciones en componentes pequeños e independientes.",
    "El análisis de impacto de cambios en software evalúa cómo las modificaciones afectan al sistema.",
    "La seguridad en bases de datos protege la información sensible contra accesos no autorizados.",
    "La integración de sistemas externos permite la interoperabilidad entre diferentes plataformas.",
    "El análisis de regresión estima las relaciones entre variables para hacer predicciones.",
    "La optimización de procesos mejora la eficiencia operativa y reduce costos.",
    "El análisis de datos estructurados organiza información en un formato fijo y predefinido.",
    "La implementación de pruebas de carga asegura que el sistema pueda manejar altos volúmenes de tráfico.",
    "La gestión de configuraciones mantiene la consistencia en los entornos de desarrollo y producción.",
    "El análisis de comportamiento del usuario proporciona información sobre cómo interactúan los usuarios con una aplicación.",
    "La implementación de técnicas de cifrado asegura que los datos estén protegidos en tránsito y en reposo.",
    "El diseño de sistemas distribuidos permite que los componentes del sistema funcionen en diferentes ubicaciones.",
    "El análisis de redes proporciona información sobre la estructura y funcionamiento de las redes de comunicación.",
    "La automatización del flujo de trabajo reduce el tiempo necesario para completar tareas repetitivas.",
    "La evaluación de rendimiento mide la efectividad de un sistema en términos de velocidad y precisión.",
    "El análisis de riesgo en proyectos ayuda a identificar y mitigar posibles problemas antes de que ocurran.",
    "La implementación de estándares de codificación mejora la legibilidad y mantenibilidad del código.",
    "El análisis de datos de ventas ayuda a identificar patrones y oportunidades de negocio.",
    "La administración de configuración de red asegura que los dispositivos de red estén correctamente configurados.",
    "El diseño de bases de datos optimiza el almacenamiento y recuperación de datos en sistemas de gestión de bases de datos.",
    "La implementación de técnicas de análisis de texto ayuda a extraer información relevante de documentos.",
    "El análisis de uso de recursos permite identificar y optimizar el consumo de recursos en sistemas informáticos.",
    "La gestión de usuarios y permisos asegura que los accesos a los sistemas sean adecuados y seguros.",
    "El análisis de eficacia de campañas de marketing proporciona información sobre el impacto de las estrategias de marketing.",
    "La implementación de técnicas de respaldo y recuperación protege los datos contra pérdidas y corrupciones.",
    "El análisis de datos de tráfico web ayuda a entender cómo los usuarios interactúan con un sitio web.",
    "La gestión de proyectos de TI asegura que los proyectos se completen a tiempo y dentro del presupuesto.",
    "La optimización de consultas SQL mejora el rendimiento de las bases de datos relacionales.",
    "El análisis de datos de encuestas proporciona información sobre las opiniones y preferencias de los encuestados.",
    "La implementación de técnicas de recuperación ante desastres asegura que los sistemas puedan recuperarse de fallos graves.",
    "El análisis de seguridad informática identifica vulnerabilidades y amenazas en los sistemas de TI.",
    "La administración de servidores asegura que los sistemas informáticos funcionen correctamente y estén disponibles.",
    "El análisis de patrones de consumo de energía ayuda a identificar oportunidades de ahorro y eficiencia.",
    "La implementación de técnicas de segmentación de mercado permite personalizar las estrategias de marketing para diferentes grupos de clientes.",
    "El análisis de datos de rendimiento de aplicaciones ayuda a identificar y solucionar problemas de rendimiento.",
    "La optimización de procesos de negocio mejora la eficiencia y reduce costos en las operaciones empresariales.",
    "La gestión de datos maestros asegura la calidad y consistencia de la información en los sistemas empresariales.",
    "El análisis de datos de comportamiento de compra proporciona información sobre los patrones de compra de los clientes.",
    "La implementación de técnicas de análisis de riesgos en proyectos ayuda a prever y mitigar posibles problemas.",
    "El análisis de datos de rendimiento de red ayuda a identificar y solucionar problemas de conectividad y velocidad.",
    "La gestión de cambios en proyectos de TI asegura que las modificaciones se realicen de manera controlada y documentada.",
    "El análisis de datos financieros ayuda a tomar decisiones informadas sobre inversiones y estrategias empresariales.",
    "Python es un lenguaje de programación muy versátil y popular.",
    "Docker facilita la creación y gestión de contenedores para aplicaciones.",
    "La inteligencia artificial está revolucionando la industria tecnológica.",
    "El aprendizaje automático es una rama de la inteligencia artificial.",
    "JavaScript es esencial para el desarrollo web interactivo.",
    "React es una biblioteca para construir interfaces de usuario en aplicaciones web.",
    "La ciberseguridad es crucial para proteger datos sensibles.",
    "Las bases de datos son fundamentales para almacenar y gestionar información.",
    "DevOps se centra en la colaboración entre desarrollo y operaciones.",
    "Los microservicios permiten desarrollar aplicaciones como una colección de servicios independientes.",
    "El análisis de datos ayuda a tomar decisiones basadas en información.",
    "El cloud computing permite acceder a recursos de computación a través de internet.",
    "Los algoritmos son secuencias de instrucciones para resolver problemas específicos.",
    "La programación funcional se basa en el uso de funciones y evita el estado mutable.",
    "Los frameworks como Django facilitan el desarrollo de aplicaciones web en Python.",
    "Las APIs permiten que diferentes aplicaciones se comuniquen entre sí.",
    "Big Data se refiere al manejo de grandes volúmenes de datos.",
    "La automatización ayuda a reducir el trabajo manual mediante el uso de tecnología.",
    "El desarrollo móvil se enfoca en crear aplicaciones para dispositivos móviles.",
    "La visualización de datos convierte datos complejos en gráficos comprensibles.",
    "La arquitectura de microservicios permite escalar aplicaciones de manera eficiente.",
    "Las técnicas de minería de datos extraen patrones útiles de grandes conjuntos de datos.",
    "El testing de software asegura que las aplicaciones funcionen como se espera.",
    "La optimización de algoritmos mejora el rendimiento de las aplicaciones.",
    "La programación concurrente permite ejecutar múltiples tareas simultáneamente.",
    "El desarrollo ágil se enfoca en entregas rápidas y continuas de software.",
    "Las redes neuronales son un componente clave del aprendizaje profundo.",
    "La integración continua automatiza la combinación de cambios en el código.",
    "El análisis de sentimiento mide las opiniones expresadas en textos.",
    "El procesamiento de lenguaje natural facilita la interacción entre humanos y computadoras.",
    "La infraestructura como código permite gestionar recursos de manera automatizada.",
    "El diseño de bases de datos optimiza la organización de la información.",
    "El scraping web extrae datos de sitios web para su análisis.",
    "La virtualización permite ejecutar múltiples sistemas operativos en una sola máquina.",
    "El control de versiones ayuda a gestionar cambios en el código fuente.",
    "La computación en la nube ofrece escalabilidad y flexibilidad en el uso de recursos.",
    "Los contenedores permiten empaquetar aplicaciones con todas sus dependencias.",
    "El análisis predictivo utiliza datos históricos para prever eventos futuros.",
    "El diseño centrado en el usuario asegura que las aplicaciones sean fáciles de usar.",
    "La programación orientada a objetos organiza el código en torno a objetos y clases.",
    "La automatización de pruebas mejora la calidad del software.",
    "La escalabilidad de aplicaciones asegura que puedan manejar aumentos en la carga.",
    "La privacidad de datos protege la información personal de accesos no autorizados.",
    "El desarrollo basado en pruebas ayuda a crear software confiable y libre de errores.",
    "La gestión de proyectos ágil facilita la adaptación a cambios durante el desarrollo.",
    "La arquitectura de software define la estructura y diseño de una aplicación.",
    "La seguridad en la nube protege los datos y aplicaciones alojados en entornos de nube.",
    "El aprendizaje profundo es una técnica avanzada de aprendizaje automático.",
    "El análisis de datos en tiempo real procesa datos a medida que se generan.",
    "La implementación continua despliega automáticamente nuevas versiones de software.",
    "El almacenamiento en caché mejora el rendimiento al guardar datos accesibles rápidamente.",
    "La recuperación ante desastres asegura la continuidad de operaciones tras fallos graves.",
    "La ingeniería de datos prepara y gestiona grandes volúmenes de información.",
    "La autenticación multifactor añade capas adicionales de seguridad al acceso a sistemas.",
    "El diseño de interfaces de usuario optimiza la experiencia del usuario en aplicaciones."
]

# Lista de tags para evaluar
#tags = ["python", "programación", "tecnologías", "lenguaje"]
tags = [
    "desarrollo web",
    "python",
    "machine learning",
    "inteligencia artificial",
    "docker",
    "bases de datos",
    "java script",
    "react",
    "devops",
    "microservicios",
    "algoritmos",
    "datascience",
    "ciberseguridad",
    "cloud computing",
    "programación funcional",
    "frameworks",
    "apis",
    "bigdata",
    "automatización",
    "desarrollo móvil"
]

# Preprocesar los documentos: convertir a minúsculas y dividir en palabras
def preprocess_document(doc):
    return doc.lower().split()

# Crear una lista de listas de palabras
docs_words = [preprocess_document(doc) for doc in documentos]

# Crear un conjunto de todas las palabras únicas en todos los documentos
all_words = set(word for doc in docs_words for word in doc)

# Calcular la frecuencia de término (TF) para cada documento
def compute_tf(doc):
    tf = Counter(doc)  # Cuenta cuántas veces aparece cada palabra en el documento
    doc_len = len(doc)  # Número total de palabras en el documento
    for word in tf:
        tf[word] = tf[word] / doc_len  # Normaliza la frecuencia de cada palabra
    return tf

# Calcular la frecuencia inversa de documento (IDF) para cada palabra
def compute_idf(docs_words):
    num_docs = len(docs_words)  # Número total de documentos
    idf = {}
    doc_count = Counter(word for doc in docs_words for word in set(doc))  # Cuenta cuántos documentos contienen cada palabra
    
    for word in all_words:
        idf[word] = math.log(num_docs / (doc_count[word] + 1)) + 1  # Calcula IDF y evita división por cero
    
    return idf

# Calcular TF-IDF para cada documento
def compute_tfidf(docs_words):
    tfidf = []
    idf = compute_idf(docs_words)  # Calcula IDF para cada palabra
    
    for doc in docs_words:
        tf = compute_tf(doc)  # Calcula TF para el documento
        tfidf_doc = {word: tf[word] * idf[word] for word in doc}  # Calcula TF-IDF para cada palabra en el documento
        tfidf.append(tfidf_doc)
    
    return tfidf

# Calcular TF-IDF
tfidf = compute_tfidf(docs_words)

# Calcular la media de TF-IDF de todas las palabras encontradas
def calculate_mean_tfidf(tfidf_list):
    all_tfidf_values = []
    for doc_tfidf in tfidf_list:
        all_tfidf_values.extend(doc_tfidf.values())
    
    if all_tfidf_values:
        return np.mean(all_tfidf_values)  # Media de todos los valores TF-IDF encontrados
    return 0

# Calcular la probabilidad de interés para cada tag
def calculate_tag_probabilities(tags, tfidf_list, mean_tfidf):
    tag_scores = {tag: 0 for tag in tags}
    num_docs = len(tfidf_list)
    
    for tag in tags:
        total_score = 0
        for doc_tfidf in tfidf_list:
            if tag in doc_tfidf:
                total_score += doc_tfidf[tag]
        
        # Calcular la probabilidad de interés ajustada por la media de TF-IDF
        mean_score = total_score / num_docs if num_docs > 0 else 0
        tag_scores[tag] = mean_score / mean_tfidf if mean_tfidf > 0 else 0
    
    return tag_scores

# Calcular la media de TF-IDF para todas las palabras encontradas
mean_tfidf = calculate_mean_tfidf(tfidf)

# Calcular la probabilidad de interés para cada tag
tag_probabilities = calculate_tag_probabilities(tags, tfidf, mean_tfidf)

# Mostrar resultados
print("Probabilidad de interés para cada tag:")
for tag, prob in tag_probabilities.items():
    print(f"{tag}: {prob:.4f}")











# Preprocesamiento de documentos y tags
def preprocess(text):
    text = text.lower()  # Convertir a minúsculas
    text = re.sub(r'\W+', ' ', text)  # Eliminar signos de puntuación
    return text

def calculate_interest(documents, tags):
    tag_count = {tag.lower(): 0 for tag in tags}
    
    # Contar frecuencia de cada tag en todos los documentos
    for doc in documents:
        doc = preprocess(doc)
        for tag in tags:
            tag = tag.lower()
            tag_count[tag] += doc.count(tag.lower())

    # Calcular la puntuación de interés para cada documento
    scores = []
    for doc in documents:
        doc = preprocess(doc)
        score = sum(doc.count(tag.lower()) for tag in tags)
        scores.append(score)
    
    return scores

# Calcular puntuaciones de interés
interest_scores = calculate_interest(documentos, tags)

# Mostrar los resultados
for i, doc in enumerate(documentos):
    print(f"Documento {i+1}:")
    print(f"  Texto: {doc}")
    print(f"  Puntuación de interés: {interest_scores[i]}")
    print()

