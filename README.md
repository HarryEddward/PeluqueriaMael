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

<img width="100px" height="100px" src="https://avatars.githubusercontent.com/u/7468980?s=200&v=4"><img height="100px" src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"><img height="60px" src="https://www.sphinx-doc.org/en/master/_static/sphinx-logo.svg"><img height="100px" src="https://camo.githubusercontent.com/18387d2dd6723fd0bdc7daf00e83f521c8b8dfe3de3476170d6f1d8d73b0e211/68747470733a2f2f692e6962622e636f2f436e386868647a2f696d6167652e706e67"><img height="80px" src="https://i.ibb.co/MsY6dDy/584807f6cef1014c0b5e48e0.png"><img height="100px" src="https://www.uvicorn.org/uvicorn.png"><img height="100px" src="https://i.ibb.co/hV3FvGk/maxresdefault.jpg"><img height="100px" src="https://docs.pytest.org/en/8.2.x/_static/pytest1.png">


Las tecnologías que uso es:
- Tornado (Framework Websocket API) + RethinkDB
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

**RethinkDB** se hará exclusivamente su úso para la app de los trabajadores para la ```obtención en tiempo real``` de las reservas de ese día, usando como API framework **Tornado** como para solo úso exlcusivo para webosocket evitando úso de fastapi, aprovechando su caracteristíca junto con RethinkDB para hacerlo mas eficiente a producción.

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

<img width="50%" src="https://i.ibb.co/q5jh7QS/Amazon-es-Pedido-402-5908292-4861967-1.png">



## Instalación_Del_Servidor
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