# Proyecto App/Web Peluquería Mael

[![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white)](#)
[![Sphinx](https://img.shields.io/badge/Sphinx-000?logo=sphinx&logoColor=fff)](#)
[![React](https://img.shields.io/badge/React-%2320232a.svg?logo=react&logoColor=%2361DAFB)](#)
[![React Native](https://img.shields.io/badge/React_Native-%2320232a.svg?logo=react&logoColor=%2361DAFB)](#)
[![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=fff)](#)


<br>
<p align="center">
  <img width="200px" height="200px" src="https://i.ibb.co/82mkyXS/Dise-o-sin-t-tulo.png">
</p>

<h3 align="center">Reserva de forma: Intuitiva, Escalable & Simple</h3>

<p align="center">
  <a href="https://peluqueriamael.com/docs"><strong>Explora en la documentación »</strong></a>
</p>
<p align="center">
  <a href="https://github.com/twbs/bootstrap/issues/new?assignees=-&labels=bug&template=bug_report.yml">Report bug</a>
  ·
  <a href="https://github.com/twbs/bootstrap/issues/new?assignees=&labels=feature&template=feature_request.yml">Request feature</a>
  ·
  <a href="https://themes.getbootstrap.com/">Themes</a>
</p>


<br>
<!--
<p align="center">
  <img src="https://mariospeluqueros.es/wp-content/uploads/2023/09/AF1QipM4by_QD-G1sdivQVIVYudYBPZvP3HPt7D_CkNg.jpg" alt="Texto alternativo">
</p> -->


# Índice

1. [App](#App)
2. [Web](#Web)
3. [Backend](#Backend)
4. [Conclusión](#conclusión)
5. [Bases_De_datos](#Bases_de_datos)
6. [Diseño_Del_Backend](#Diseño_del_backend)
7. [Distribución_De_Software](#Distribución_De_Software)
8. [Presupuesto_Pc_Servidor](#Presupuesto_Pc_Servidor)
9. [Factura_De_La_Compra](#Factura_De_La_Compra)
10. [Instalación_Del_Servidor](#Instalación_Del_Servidor)
11. [Configuración_Del_Servidor](#Configuración_Del_Servidor)
12. [Créditos](#Créditos)


## *Nombre actual: PeluqueríaEGO

### Es una App/Web para la *PeluqueríaMael úbicada en Inca, Mallorca, Islas Baleares.

Hecho por **Adrià Martín Martorell**, como una práctica como freelancer de forma
autodidáctica. No sonsiderado un trabajo, sino una venta hecha como particular.
En el año que lo hize y acabé tengo 17 años.

## App
El propósito de la app es ```crear reservas de forma automática```, sin intervención
manual. Simplemente todo de forma autonoma, y los clientes simplemente puedan
reservar de la forma mas simple y intutuitiva para los clientes, y los trabajadores pueda saber rápidamente
sus reservas en tiempo real.

Hago uso de una tecnología cross-platform para evitar doble código. Y como no se require
de caracterisitcas de una app muy avanzadas, simplemente así mejora la mantenabilidad y hace único el codigo fuente.

En la app no simplemente se queda en hacer una app, sino dividir en difernetes apps, por su úso:
- Administrador
- Trabajadores
- Clientes

La tecnología que uso es un framework cross-platform de js, llamada ```React Native```. Usando tsx como
código mantenible por un mismo lenguaje de frontend de base, como la web y la misma app.

Esta hecho por react-native cli, y usando stores con zustand. Mientras guardar los datos de forma persistente hará úso de Sqlite

## Web
El proposito de la web es acceder en ella y descargar de forma simple la app, y
hacer uso de links promocionales o de información para hacer uso en las redes sociales
de la peluquería

## Backend
El backend se hizo separado por el forntend haciendo una RestAPI, separado de forma independiente,
así evitando modularizando mucho mas el código y incluso mejorando el rendimiento del mismo.



<img height="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"><img height="60px" src="https://www.sphinx-doc.org/en/master/_static/sphinx-logo.svg"><img height="100px" src="https://camo.githubusercontent.com/18387d2dd6723fd0bdc7daf00e83f521c8b8dfe3de3476170d6f1d8d73b0e211/68747470733a2f2f692e6962622e636f2f436e386868647a2f696d6167652e706e67"><img height="80px" src="https://i.ibb.co/MsY6dDy/584807f6cef1014c0b5e48e0.png"><img height="100px" src="https://www.uvicorn.org/uvicorn.png"><img height="100px" src="https://i.ibb.co/hV3FvGk/maxresdefault.jpg"><img height="100px" src="https://docs.pytest.org/en/8.2.x/_static/pytest1.png"><img height="80px" src="https://i.ibb.co/vB4krcw/expressjs-ar21.png">  <img height="80px" src="https://i.ibb.co/3RwqcCz/logo.png">


Las tecnologías que uso es API (Estática):
- FastAPI (Framework Full API)
- Pydantic
- Gunicorn (Producción)
- Uvicorn (Desarrollo)
- Fastapi_cache[redis]
- Redis
- PyMongo
- Ujson
- PyJWT
- Fastapi_limiter
- To_literal (Creador de la libreria) [https://github.com/HarryEddward/to_literal]
- Sphinx
- Pytest
- Unitest
- RethinkDB
- Numpy

Las tecnologías que uso es APIWS (Websockets):
- Express.js
- Socket.io
- RethinkDB
- Http
- Jsdocs

(**Comentar que haré una libreria en Node.js un framework de una API completamente de WebSOcket usando Socket.io como dependencia, realmente con Express-ws no fuñe realmente bien, en un futuro, no me gustó para nada manejar con scoekt.io de esta forma**)

Las tecnologías que uso es API (Estática Criptográfica):
- FastAPI
- Pycuda
- Numpy
- Crypto
- Uvicorn

Haciendo uso de un backend moderno, y fácil de mantener, y uno de los mas rapidos de Python.
Teniendo un íncreible rendimiento por su lenguaje de alto nivel, superando a Express.js y a node.js.

Implemente mi propio middleware que restringe un grupo de rutas especificas, que implemente doble auth
con jwt. En ```.../config/middleware/restricted.py```. Es extremadamente extricto al hacer cualquier operación
del usuario, y protegiendo la misma información renovando por cada operación su propia clave secreta del jwt
que cada usuario tiene. Así preveniendo ataques masivos y multioperaciónes no autorizadas.

## Bases_De_Datos

<p align="center">

<img height="100px" src="https://i.ibb.co/8bN03FF/mongodb-logo-1-1-30.png">

<img height="100px" src="https://img.stackshare.io/service/531/Sp0fIxul_400x400.jpg">

<img height="100px" src="https://i.ibb.co/QX9kmhT/redis-logo.png">

</p>


Hago uso de 2 bases de datos, de forma local:
- Redis
- MongoDB
- RethinkDB

**Redis** para el almacenamiento temporal de ```caché```, mientras que **MongoDB** una base de datos ```persistente```
para guardar todos los datos de forma ordenada, flexible, y rapida. Haciendo úso en FastAPI.

**RethinkDB** se hará exclusivamente su úso para la app de los trabajadores para la ```obtención en tiempo real``` de las reservas de ese día, usando como API framework **Express.js + Socket.io** como para solo úso exlcusivo para webosocket evitando úso de fastapi, aprovechando su caracteristíca junto con RethinkDB para hacerlo mas eficiente a producción.

Juntando dos diferentes mundos pero separado, con su íncreible asíncronidad.

## Diseño_Del_Backend
Tiene una estructura dividida por microservicios, separado por diferentes versiónes para futuras
actualziaciones que se hagan


## Distribución_De_Software
Modelo de distribución de software hacia la peluquería:
- IaaS

Modelo de distribución de software de la peluquería hacía sus clientes:
- SaaS


## Presupuesto_Pc_Servidor
Creé un presupuesto ajustado de 550€, y realmente priorize la baja latencia entre la potencia misma del pc, y tuvé como conclusión que realmente invertir en mejorar la baja latencia sea una parte crítica del servidor web. Y para evitar la perdida de datos en malas condiciónes como en tormentas o en fluctuaciónes de tensiónes el mismo SAI protegería al mismo PC.

Aquí esta el presupuesot hecho para el dueño de la peluquería, para Mael, buscando en Pcomponentes. 
```(Los precios y productos puede ser que no aparezcan o no sean los mismos)```

<p align="center">
  <img width="60%" height="60%" src="https://i.ibb.co/2jtGPvW/Presupuesto-servicios-creativos-simple-blanco-y-celeste-2.png">
</p>

## Factura_De_La_Compra
Quizás te hayas preguntado si esto es simplemente es un montaje? No y para que me creaís, ponga la factura de Amazon con los datos, están censurados por motivos de seguridad y privacidad.

<img width="50%" src="https://i.ibb.co/q5jh7QS/Amazon-es-Pedido-402-5908292-4861967-1.png"><img width="50%" src="https://i.ibb.co/72JBv6b/Amazon-es-Pedido-402-5908292-4861967-2.png">


## Instalación_Del_Servidor
Usare Cubic in Launchpad, haré mi propio os personalizado

## Caracteríticas_Técnicas_Y_Montaje_Del_Hardware
La instalación consistiría 2 mini pc de sobremesa con un procesador de N100 con 16GB cada uno. Para mejorar las operaciónes de criptografía y no sobrecargar la carga central de mismo pc, se hace uso de una gráfica GT 710 con 1GB sea suficiente para no sobrecargarlo. Como no se hará úso de interfaz gráfica se dedicará con un script de python para encriptar y desencriptar con el úso de la gpu, y preocuparando no hace run cuello de botella.

Entre los 2 pc, se hace un sistema maestro & esclavo, consiste en conectar el cable de ethernet al 1r pc y luego conectar el 1r al 2n, pero teniendo en cuenta que los 2 pc deben de estar conectados al ethernet. Pero a la hora de coordinar las peticiónes con docker-swarm se tendra en cuenta de esta forma.

El 2n pc se le quita la RAM que tiene instalada del minipc para insertar el adapatado de la gráfica, es verdad que reduces la cantidad de memoria disponible, pero como no es el pc maestro no hay que procuparse, y tendrá una API dedicada en ese pc, para tareas de cryptografía. Como encriptar y desencriptar, pero así mejora la seguridad porque como el pc esta separado y de forma interna sin estar esta API expuesto a ethernet evitaríamos ataques de fuera.

Y se utilizarían 3 cables ethernet uno de CAT 8, mientras que otro por CAT 6a, mientras entre pc debe de ser instanteanea, entre el router, por la velocidad del ethernet va bien que sea CAT 6a por la velocidad que tiene.

<p align="center">
  <img width="110px" height="110px" src="https://i.ibb.co/gWtSfTr/61y-D0tp4-GCL-AC-AA360.jpg">
  <img width="110px" height="110px" src="https://i.ibb.co/VHMyQp5/71z-ZVl0dj4-L-AC-AA360.jpg">
  <img width="110px" height="110px" src="https://i.ibb.co/FDgpgWF/51vn-NQp56-QL-AC-AA360.jpg">
  <img width="110px" height="110px" src="https://i.ibb.co/VwrpXpf/61-GDv-Jm-GF5-L-AC-AA360.jpg">
  <img width="110px" height="110px" src="https://i.ibb.co/71wC7mR/61f9r59-Chr-L-AC-AA360.jpg">
  <img width="110px" height="110px" src="https://i.ibb.co/X4QXWSg/41sw-Rzq-Jbd-L-AC-AA360.jpg">
</p>

**IMPORTANTE:**
Los mini pc estan trucados internamente, para que no peudas poner ningún os, y incluso ni siquiera wsl. Claramente así no puedo trabajar ya que con Docker-swarm no me funciona de forma correcta. Si que por aprovechar 2 minipc barratos, acabe pagando mas en tiempo que en dinero.
Suelen estar a 199€ por algún buen motivo.

Devolveré los 2 minipc mas el adaptador de la gráfica

Realizé 3 docuementos al dueño de la peluquería, informando el estado de los productos comprados para el pc, luego otro documento especificando los productos a devolver y por último, el presupuesto renovado para el nuevo pc.

<p align ="center">
  <img width="45%" src="https://i.ibb.co/3YbhcPp/Informe-pc-de-servidor.png">
  <img width="45%" src="https://i.ibb.co/kHf57kF/Presupuesto-Renovado.png">
  <img width="45%" src="https://i.ibb.co/7W4tT5K/Devolucion-del-presupuesto.png">
</p>

## Devolución_de_productos_sin_úso
La devolución se hara por SEUR, y le tenemos que dar el mismo producto a la oficina en Palma. Se realiza la devolución con las mismas cajas enviadas.

Como estoy haciendo prácticas a una tienda de electrónica, no me puedo encargar yo. Pero mi cliente tampoco sabe muy bien manejar la informatica.

La solución fué imprimir los qr de seur es pegarlos por las 2 cajas, y así directamente cuando mi cliente pueda devolverlos a seur no tenga ningún problema ya que el mismo contenido esta dentro de las mismas cajas.

<p align="center">
  <img width="50%" src="https://i.ibb.co/KqZjzqf/IMG-20240528-152238.jpg">
</p>


## Performance de encritpación
A la hora de hacer la api de encriptación (CryptoAPI), haciendo por separado 2 Routers, uno para la cpu y la otra
para la gpu. Hice intencionalmente la cpu por si algún motivo la gpu deja de funcionar, y evitar depender de varios
dispositivos.
Inicie un testeo rápido por encima el performance que tendría que entre los 2 tipos de formas en encriptación por
diferentes dispositivos.
El resultado es el siguiente:

  - CPU: MacBookAir (Sonoma 14.1.1): 18-20s por 100 encriptaciónes y 100 decriptaciónes
  - GPU: i5 9gen, solo por GPU(gt-710): 8.9s por 1000 encriptaciónes y 1000 decriptaciónes

Decir que la MacBookAir estaba ya con mucho estrés, pero como las cpu's de las mac suelen ser mas eficientes que las
de intel, por su propia inteligenic artificial que mejora mucho los procesos, no esta nada mal.

La gpu realmente puede tener cargas de trabajo intensivas a la criptografía sin ningún problema y es mucho mas
eficiente y prometedor que la misma cpu que aparte lo sobrecarga de mas.

Podríamos decir que el % de mejora es muy alto de un **+368.42%** en tareas criptográficas por la GPU
Use el repositorio de github llamado (Cuda-AES) y modifique para en vez de usar su cli, lo convirtiese en un código
mas senzillo de implementarlo importarlo en otro código en el archivo principal de AES.py

Repo: https://github.com/aranscha/CUDA-AES

Haré una librería para tener una fácil implementación de ecnriptación por gpu a través de esta repo
con creditos todos suyos, para que cualquiera pueda implementarlo al escargar la librería de forma fácil
de descargarlo y implementarlo. Lo llamaré easy_cuda_crypto_gpu


### 23/6/2024
Conseguí hacer la libreria de encritpación en 1 día de python para úso de GPU, se llama: gpu_cuda_aes. Es fácil de usar y consigua alcanzar niveles grandes de rendimiento por simple úso de la GPU. Estará listo para publicarse hoy mismo luego de añadir los docs, el testeo y lo compile!
Así evito dependencias por repositorios y ayudo a la misma comunidad, aparte de un código mas simple y legible.

## Docker
Hare úso de docker-swarm, por el hecho que se autogestióna por el mismo. No es
tan complejo como kubernetes y por la simplicidad de la tecnología, y el úso a
producción a nivel regional no sera necesario la capacidad de hacer úso de muchos servidores.

## Testing
Por cada API que se hace tiene su apartado de tesetos, en caso de Python se usa pytest y httpx. Y el directorio donde se hacen
los testeos dentro del API estan dentro de la misma versión que se usa. Se llama: ```__tests__```

## Configuración_Del_Servidor
Usó Linux como OS predeterminado para el servidor, tengo pensado en el futuro adaptarselo con FreeBSD por su alto performance y úso nativamente de contendores llamado jails en FreeBSD.

## Créditos

<p align="center">
  <a href="https://gravatar.com/au7812ooae32">
  <img width="120px" height="120px" src="https://pypi-camo.freetls.fastly.net/36f397b09a7781d43d862d849361e2e6ae718ca6/68747470733a2f2f7365637572652e67726176617461722e636f6d2f6176617461722f39663431306239623365363937333832303965366131343163636137623339653f73697a653d313430">
  </a>
</p>
<p align="center">
  <a href="https://www.instagram.com/__adrian__martin__/"><b>Instagram</b></a> ·
  <a href="https://pypi.org/user/AdriaMartin/"><b>PyPi</b></a> ·
  <a href="https://gravatar.com/au7812ooae32"><b>Profile</b></a> ·
  <a href="https://github.com/HarryEddward/to_literal"><b>Github</b></a>
</p>
<p align="center">
  <span><b>Desarrollador frontend</b></span> -
  <span><b>Desarrollador backend</b></span> -
  <span><b>Desarrollador devops</b></span> -
  <span><b>Instalador</b></span> -
  <span><b>Configurador</b></span>
</p>