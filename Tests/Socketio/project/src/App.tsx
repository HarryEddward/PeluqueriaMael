import React, { useEffect, useState } from 'react';
import socketIOClient from 'socket.io-client';
import ReservasList from './components/ReservasList';

const ENDPOINT = "http://localhost:3000";

interface Reserva {
  id: string;
  nombre: string;
  fecha: string;
}

interface Change {
  new_val: Reserva | null;
  old_val: Reserva | null;
}

const App: React.FC = () => {
  const [reservas, setReservas] = useState<Reserva[]>([]);

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT);

    const handleInitialData = (data: Reserva[]) => {
      // Establecer las reservas iniciales
      setReservas(data);

      // Desconectar el evento de initial_data
      socket.off('initial_data', handleInitialData);

      // Ahora suscribirnos a las actualizaciones en tiempo real
      socket.on('data_update', (change: Change) => {
        setReservas(prevReservas => {
          const updatedReservas = [...prevReservas];

          if (change.old_val && !change.new_val) {
            // Eliminar la reserva (delete)
            return updatedReservas.filter(reserva => reserva.id !== change.old_val!.id);
          } else if (change.old_val && change.new_val) {
            // Modificar la reserva (update)
            const index = updatedReservas.findIndex(reserva => reserva.id === change.old_val!.id);
            if (index !== -1) {
              updatedReservas[index] = change.new_val;
            }
          } else if (!change.old_val && change.new_val) {
            // Añadir nueva reserva (insert)
            updatedReservas.push(change.new_val);
          }

          return updatedReservas;
        });
      });
    };

    // Recibir los datos iniciales primero
    socket.on('initial_data', handleInitialData);

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      <h1>Reservas en tiempo real</h1>
      <ReservasList reservas={reservas} />
    </div>
  );
}

export default App;
