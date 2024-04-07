# Descripción de Tipos de Error

A continuación se describen los diferentes tipos de errores que pueden ocurrir en la aplicación y cómo pueden ser manejados:

- **SUCCESS**: Indica que la operación se realizó correctamente.
  - *Descripción*: Esta es una señal de que la operación se completó con éxito sin ningún problema. No se requiere ninguna acción adicional.

- **DATABASE_ERROR**: Indica que hubo un error al interactuar con la base de datos.
  - *Descripción*: Este tipo de error sugiere que la operación falló debido a un problema con la base de datos. Puede ser necesario revisar los registros del sistema o contactar al administrador de la base de datos para resolver el problema.

- **MISMATCH**: Indica que los detalles de la cita no coinciden.
  - *Descripción*: Este tipo de error ocurre cuando se intenta cancelar una cita pero los detalles de la cita no coinciden con la información almacenada en la base de datos. Se recomienda verificar los detalles de la cita antes de intentar cancelarla nuevamente.

- **NO_APPOINTMENT**: Indica que no hay una cita programada en el horario especificado.
  - *Descripción*: Este tipo de error ocurre cuando se intenta cancelar una cita pero no existe ninguna cita programada en el horario especificado. Se recomienda verificar el horario y la fecha de la cita antes de intentar cancelarla nuevamente.

- **NO_AVAILABILITY**: Indica que no hay disponibilidad para programar una cita en el horario solicitado.
  - *Descripción*: Este tipo de error ocurre cuando se intenta programar una cita pero no hay disponibilidad de horario para el profesional seleccionado en el período especificado. Se recomienda verificar el horario disponible del profesional o intentar programar la cita en otro momento.

- **ERROR1**: `INVALID_PERIOD`
  - *Descripción*: Indica que el período especificado no es válido para este profesional.

- **ERROR2**: `AFTERNOON_CLOSED`
  - *Descripción*: Indica que no se puede programar una cita en la tarde antes del mediodía.

- **ERROR3**: `MORNING_CLOSED`
  - *Descripción*: Indica que no se puede programar una cita en la mañana después del mediodía.

- **ERROR4**: `AFTERNOON_OVERBOOKED`
  - *Descripción*: Indica que no se puede programar la cita para el profesional después del horario de cierre de la tarde.

- **ERROR5**: `MORNING_OVERBOOKED`
  - *Descripción*: Indica que no se puede programar la cita para el profesional después del horario de cierre de la mañana.

- **ERROR6**: `OVERLAPPING_APPOINTMENTS`
  - *Descripción*: Indica que no se puede programar la cita para el profesional en la franja horaria solicitada.

- **JWT_CODIFY_ERROR**:
  - *Descripción*: Error al codificar el token jwt

- **JWT_ERROR**:
  - *Descripción*: Error general al codificar/expirar el token jwt, no específica el problema.

- **JWT_EXPIRED_ERROR**:
  - *Descripción*: Error en la expiración del token jwt




*return* {
  `"info"`: **"Informa de que trata exactamente el error"**,
  `"status"`: **"no/ok"**,
  `"type"`: **"Tipo de error específico"**  -- Úbicado en ERRORS.md, aquí --
}

