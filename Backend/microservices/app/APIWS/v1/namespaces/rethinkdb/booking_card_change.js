const { router } = require('../../server');
var colors = require('colors');


router_prefix = router("/booking_card_change");

const Router = (io) => {
    io.of(router_prefix)
    .on('connection', (socket) => {
        
        socket.on('init', (data) => {
            console.log(data);
        });

        socket.on('disconnect', () => {
            console.log('Client disconnected from booking card namespace');
        });

    });
};

module.exports = {
    Router,
    router_prefix
}