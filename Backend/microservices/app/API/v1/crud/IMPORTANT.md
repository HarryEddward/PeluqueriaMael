# CRUD IMPORTANT

En el crud no es lo mismo que las rutas, hize en todos los archivos
instancias con __init__() por cada parte del crud, y no como el `__init__() no devuelve nada`, hacemos uso de `self.response` para acceder a los datos.

Lo explico porque realmente en la estructura de las condicionales cuando
uno devuelve algo suele ser mas verboso, y no tiene la msima estructura cuando
uno hace uso de @classmethod.

**Hace uso de una variable, no un return.**
Es una instancia de un objecto, no es una función.

Ejemplo:

· Ejemplo correcto 👍

if **not** user:
    self.response = {
        "info": "",
        "status": "no",
        ...
    }
else:
    self.response = {
        "info": "",
        "status": "ok",
        ...
    }

//Rest of the code


· Ejemplo incorrecto 👎

if **not** user:
    self.response = {
        "info": "",
        "status": "no",
        ...
    }

self.response = {
    "info": "",
    "status": "ok",
    ...
}

//Rest of the code


Especificar que en el ejemplo incorrecto, aunque este mal la vairable a lo largo del
código se va cambiando y no se hace uso de un return.