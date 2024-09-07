// swaggerDoc.js
/**
 * @swagger
 * components:
 *   schemas:
 *     WebSocketResponse:
 *       type: object
 *     StatusResponse:
 *       type: object
 *       properties:
 *         info:
 *           type: string
 *           description: Info about server status.
 *         status:
 *           type: string
 *           description: Status message.
 */

/**
 * @swagger
 * (ws)/rethinkdb/booking_card_change:
 *   trace:
 *     summary: Check the status of the server.
 *     tags: [Status]
 *     responses:
 *       -:
 *         description: .
 *         content:
 *           WebSocket:
 *             schema:
 *               $ref: '#/components/schemas/WebSocketResponse'
 */

