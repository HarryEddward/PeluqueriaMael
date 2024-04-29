# BACKEND

Que es un submicroservicio?:
Es que los submicroservicios, es un microservicio donde esta el crud y los submicroservciios son las rutas, un microservicio es en mi caso del API separado en diferentes rutas, y un microservicio, es un servicio en si pero dentro las rutas están separadas por diferentes servidores, asi manteniendo el microservicio para que luego en docker compose en si uno es como un microservicio y los submicroservicios que haya dentro del backend que seria los diferentes servidores de diferentes rutas, poder implementarlo todo en un archivo docker compose como un microservicio.

Por cada docker-compose.yml es un microservicio
Y por cada servicio dentro del docker-compose son submicroservicios, servicios del microservicio