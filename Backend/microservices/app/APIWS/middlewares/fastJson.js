/*const { parse } = require('fastjson');

const fastJsonMiddleware = (req, res, next) => {

    if (req.headers['content-type'] === 'application/json') {
        let data;
        try {
          data = parse(req.body);
        } catch (err) {
          return res.status(400).json({ error: 'Invalid JSON' });
        }
        if (data.err) {
          return res.status(400).json({ error: 'Invalid JSON' });
        }
        req.body = data.value;
    }
    next();

}

module.exports = fastJsonMiddleware;
*/