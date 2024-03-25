# CONFIGURACIÓN


## PORT FORWARDING
**HTTP** | PORT: 9712 `Frontend`

**HTTP** | PORT: 7878 `Backend`

## JWT

*PyJWT nunca intentar nombrar con "jwt.py" un archivo para hacer uso de jwt*
Los JWT siempre seran creados con la clase `Token`
**Són validos a partir de 120 semanas**

### Importante configurar en el servidor añadir el SECRET del JWT dentro del conteendor de Docker

En docker compose, si tendremos que definir que se ejecute en el background le
diremos a partir que lo ejecutemos en el cmd: `docker-compose up -d`