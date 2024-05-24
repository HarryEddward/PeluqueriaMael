const _ = "/worker/public";

const io = require('../../../server');
const r = require('../../../db/database');


const bookingCard = io.of(_ + "/booking_card");
bookingCard.on('connection', (socket) => {

    console.log('Cliente conectado al espacio de chat de booking_card');


    socket.on('disconnect', () => {
        console.log('Cliente desconectado del espacio de chat');
    });
});