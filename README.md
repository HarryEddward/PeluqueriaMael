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
5. [Databases](#Databases)
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

(**Comentar que haré una libreria en Node.js un framework de una API completamente de WebSocket usando Socket.io como dependencia, realmente con Express-ws no fuñe realmente bien, en un futuro, no me gustó para nada manejar con socket.io de esta forma**)

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

## How_the_structure_of_the_project_is_done?

<img width="100%" src="https://github.com/HarryEddward/PeluqueriaMael/blob/main/Github/img/microservices.png?raw=true">


## Why_will_appointments_never_be_incompatible?
Highlight that the organized work in this scheme on mongodb

<img width="100%" src="https://github.com/HarryEddward/PeluqueriaMael/blob/main/Github/img/howworkstheform.png?raw=true">


## How_APIs_relate_to_DBs
Is not that simple

<img width="100%" src="https://github.com/HarryEddward/PeluqueriaMael/blob/main/Github/img/relation_db.png?raw=true">


## Do_cybercriminals_have_any_chance_of_decrypting_data?
Yes, but an very extreme mode
<img width="100%" src="https://github.com/HarryEddward/PeluqueriaMael/blob/main/Github/img/ID_JWT.png?raw=true">

## Databases

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
- PaaS

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
I use a preset of Ubuntu to do an automatic installation in all of the computers to implement in the server. To automatize all of the installation and if the manager want in the future add others servers, implement an estandard installation of all from his servers.
To avoid wasting time dedicate to installing all dependencies they need to implement to run
correctly when all servers need to turn on to directly implement from ansible the dependecies 

## Technical_Characteristics_And_Hardware_Setup
The setup would consist of 2 mini PCs with N100 processors, each with 16GB of RAM. To improve cryptographic operations and avoid overloading the central processing unit, a GT 710 graphics card with 1GB of memory would be used. Since no graphical interface would be used, a Python script would be dedicated to encrypting and decrypting using the GPU, ensuring that there are no bottlenecks.

Between the two PCs, a master-slave system would be implemented, consisting of connecting an Ethernet cable from the first PC to the second PC, but with the understanding that both PCs must be connected to the Ethernet. However, when coordinating requests with Docker-Swarm, this setup would be taken into account.

The second PC would have its existing RAM removed and replaced with an adapter for the graphics card. Although this would reduce the available memory, as it is not the master PC, it would not be a concern. The second PC would have a dedicated API for cryptographic tasks, such as encrypting and decrypting. This would improve security because the PC would be isolated and internally exposed to the API, preventing external attacks.

Three Ethernet cables would be used: one CAT 8 and two CAT 6a. The cable between PCs should be instantaneously fast, while the router cable can use CAT 6a due to its speed.

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

## Return_Of_Products_Without_Use
La devolución se hara por SEUR, y le tenemos que dar el mismo producto a la oficina en Palma. Se realiza la devolución con las mismas cajas enviadas.

Como estoy haciendo prácticas a una tienda de electrónica, no me puedo encargar yo. Pero mi cliente tampoco sabe muy bien manejar la informatica.

La solución fué imprimir los qr de seur es pegarlos por las 2 cajas, y así directamente cuando mi cliente pueda devolverlos a seur no tenga ningún problema ya que el mismo contenido esta dentro de las mismas cajas.

<p align="center">
  <img width="50%" src="https://i.ibb.co/KqZjzqf/IMG-20240528-152238.jpg">
</p>


## Encryptation_Performance
When creating the CryptoAPI, I intentionally created two separate routers, one for CPU and one for GPU, in case the GPU fails and to avoid relying on multiple devices.

I ran a quick test to compare the performance of encryption between the two types of devices. The results are as follows:

  - CPU: MacBook Air (Sonoma 14.1.1): 18-20 seconds for 100 encryptions and 100 decryptations
  - GPU: i5 9th gen, using only the GPU (GT-710): 8.9 seconds for 1000 encryptions and 1000 decryptations

I want to note that the MacBook Air was already under heavy load, but since Mac CPUs tend to be more efficient than Intel CPUs due to their artificial intelligence that improves processes, it's not bad.

The GPU can handle intense cryptography loads without any issues and is much more efficient and promising than the same CPU, which would overload it even more.

We could say that the improvement is extremely high, with a **+368.42%** increase in cryptographic tasks using the GPU.

I used the GitHub repository called Cuda-AES and modified it to convert it into a simpler code that can be easily implemented in another code in the main AES.py file.

Repo: https://github.com/aranscha/CUDA-AES

I will create a library for easy implementation of GPU encryption through this repo, giving credits to its original authors, so that anyone can easily implement it by downloading and integrating it. I'll call it easy_cuda_crypto_gpu.


### 23/6/2024
I was able to create a library for encryption on a GPU in just one day of Python usage. It's easy to use and achieves high performance levels with simple GPU usage. It will be ready for publication today after adding documentation, testing, and compilation!

This way, I avoid dependencies on repositories and help the community, along with a simpler and more readable code.

### Library almost already for release 
The repo is already usable, but not adapted for public use on PyPi. Repo: https://github.com/HarryEddward/gpu_cuda_aes

## Docker
I will use Docker Swarm, as it automates itself. It's not as complex as Kubernetes, and its simplicity makes it suitable for regional production-level use without requiring capacity to manage many servers.

## Testing
Each API has its own testing section. For Python, we use pytest and httpx. The testing directory is **located inside the same version used within the API** and is called ```__tests__```. We use it in Python and JavaScript; while Python doesn't conventionally apply it this way, we standardize API's in this manner within the project.

## Documentation
Python APIs use Sphinx to write documentation using docstrings with a Google-standardized format. For JavaScript APIs, we will use the jsdocs library.


## Server_Configuration
We used Linux as the default OS for the server, with plans to adapt it to FreeBSD in the future due to its high performance and native support for containers called jails in FreeBSD.


## Errors during in the process

(8-8-2024)

I fix the hardest errors during the deployment test, i already fix the connection with mongodb in the separate container with have separate the docker-compose file with all of the db.
And the error was that: 


```json
{
    "info": "0.0.0.0:27017: [Errno 111] Connection refused (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms), Timeout: 30s, Topology Description: <TopologyDescription id: 66b327d8a6bb8c941f15567b, topology_type: Unknown, servers: [<ServerDescription ("0.0.0.0", 27017) server_type: Unknown, rtt: None, error=AutoReconnect("0.0.0.0:27017: [Errno 111] Connection refused (configured timeouts: socketTimeoutMS: 20000.0ms, connectTimeoutMS: 20000.0ms)")>]>",
    "status": "no",
    "type": "UNKNOWN_ERROR"
}
```
I found the solution it was more easier than i was thought, i change the host conection from the main pc from to bridge the connection within the containers to put the name of the container and specify in the docker compose yml the exact network bridge to connect with the other :

/PeluqueriaMael/Backend/microservices/app/API/v1/deployment/docker-compose.yml:
```yml
networks:
  db_hairdresser_network:
    external: true
```

/home/adrian/Documentos/PeluqueriaMael/Backend/microservices/db/docker-compose.yml:
```yml
networks:
  hairdresser_network:
    driver: bridge
```

## Confidential_Proxy
(11/9/2024)
Today I thought about how safe is to send data from the backend to the cient and backwards. And
I have the greate idea to implement in docker a single proxy container with Tor, and independently use in the API if the client want or not.

I fix some shell's scripts (run.sh) from the folder DevOps/docker/__production__, and replace to simple shell's scripts named "execute.sh" to tests all of the docker-compose.yml files in a simple way to maintain and fix more fast the error's from the new files created.


<p align="center">
  <img width="100%" height="100%" src="https://github.com/HarryEddward/PeluqueriaMael/blob/main/Github/img/tor_test_api.png">
</p>


## Ethernet Configure

By using the router's external APIs, the provider gives us the option to redirect internal ports used by the router with its connected internal devices for external use from the internet. In this way, redirecting ports with the assigned device IP allows it to be redirected to the same router with its designated port for use from the internet, starting from the Public IP that is accessed by the router. The problem with many internet service provider companies is the reduction of costs and scarcity of Public IPs; the contracts for providing internet to individuals do not permit a Public IP to be assigned, as the internet usage is deemed sufficient. Clearly, the technology they use is called CGNat, which assigns private IPs to their clients from a single Public IP. 

The hair salon apparently had a contract with Yoigo as a company that did not have a Public IP assigned, incurring unnecessary expenses and offering lower speeds compared to the company Digi in Spain, which provides better service and higher speeds for a lower cost. Therefore, the hair salon changed companies for this reason. After contracting Digi as an individual, it is supposed that you must pay an additional €1 for them to assign you a Public IP with the existing fiber contract. 

Having completed the installation without any issues, I investigated whether the router is within a CGNat network from my MacBook using the CLI command: traceroute. Through several connections, I found that it still has CGNat in use, and from the analysis, I determined that due to the jump from the router's private route to a similar one (10.0.0.1) and then to the Public IP accessing the internet, the router cannot freely expose ports.

```bash
adrian@adrian-MD34443-C943:~$ traceroute google.com
traceroute to google.com (142.250.184.174), 64 hops max
  1   192.168.1.1  1,177ms  0,755ms  0,847ms # Redirect the decive to my router
  2   10.0.**.**  14,331ms  13,578ms  16,733ms # Here are the Private IP assigned to my router
  3   172.**.**.*  10,492ms  9,470ms  9,619ms # Public IP to after access the ethernet
  4   *  *  * 
  5   *  *  * 
  6   *  *  * 
  7   91.232.81.211  32,777ms  26,822ms  25,303ms 
  8   108.170.252.225  28,749ms  28,203ms  27,866ms 
  9   142.250.213.125  26,197ms  25,447ms  25,148ms 
 10   142.250.184.174  35,974ms  44,741ms  75,778ms 
```


## License

[Apache License](https://github.com/HarryEddward/PeluqueriaMael/blob/main/LICENSE)



## Credits

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


