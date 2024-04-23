from pydantic import BaseModel
from typing import List

class workerLessBusy:

    class structure(BaseModel):
        rama_profesionales: List[str]
        professionals: dict

    def __init__(self, data: structure) -> None:

        try:
            ocupacion_profesionales = []

            data = data.model_dump()
            rama_profesionales = data["rama_profesionales"]
            professionals = data["professionals"]["professionals"]

            print('professionals->', professionals)

            '''
            Cuando se modifica los trabajadores en la parte de el array de cada uno de los profesionales,
            los nuevos dias que se crean se hacen con los nuevos trabajadores 
            '''

            for profesional in rama_profesionales:
                contador_ocupado = 0
                for periodo in professionals[profesional]:
                    for hora, estado in professionals[profesional][periodo].items():
                        if estado["status"] == "ocupado":
                            contador_ocupado += 1
                ocupacion_profesionales.append((profesional, f"{contador_ocupado/2}h")) #Se divide en 2, porque hacemos uso de 30', y tendremos una hora por 2 medias horas

            ocupacion_profesionales.sort(key=lambda x: x[1])

            self.response = {
                "info": "Entragado los profesionales menos ocupados",
                "status": "ok",
                "type": "SUCCESS",
                "data": ocupacion_profesionales
            }
        except Exception as e:
            self.response = {
                "info": f"Error desconocido: {e}",
                "status": "no",
                "type": "UNKNOW_ERROR"
            }