import React from 'react';

interface Reserva {
  id: string;
  nombre: string;
  fecha: string;
}

interface ReservasListProps {
  reservas: Reserva[];
}

const ReservasList: React.FC<ReservasListProps> = ({ reservas }) => {
  return (
    <div>
      {reservas.length > 0 ? (
        <ul>
          {reservas.map((reserva, index) => (
            <li key={index}>
              <p><strong>ID:</strong> {reserva.id}</p>
              <p><strong>Nombre:</strong> {reserva.nombre}</p>
              <p><strong>Fecha:</strong> {reserva.fecha}</p>
              <hr />
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay reservas</p>
      )}
    </div>
  );
}

export default ReservasList;
