const path = require('path');
const fs = require('fs');

const md5 = require('md5');
const serveIndex = require('serve-index');
const express  = require('express');
const router = express.Router();

class WebError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

// Maybe make this an envvar. I don't know what the young'uns mean by cloud 
// native but im pretty sure all they got in their brains are clouds anyways
const ENTRY_KEY = 'XbcuJevW$9oOvMXdLgW9NohL1fxpj#qvp%LRrBt#4SK%qtOjPP%fTSVNDyplPejp';

router.use((req, _, next) => {
  if (req.query.key != ENTRY_KEY) {
    req.session.bad_apple = true; // these are some bad apples
    req.session.report_key = process.env.REPORT_KEY || 'misconfigured yikes';
    throw new WebError(403, "No!");
  }
  return next();
});

router.get('/', (_, res) => {
  res.render('admin.html');
}); 

router.post('/', (req, res) => {
  if (req.body.username == process.env.ADMIN_USERNAME 
    && req.body.password == process.env.ADMIN_PASSWORD) {
      req.session.ADMIN_KEY = process.env.ADMIN_KEY;
  } else {
    throw new WebError(403, "Incorrect Username and Password");
  }

  res.render('logged_in_admin.html');
});

router.get('/report', (req, res) => {
  if (req.session.ADMIN_KEY != process.env.ADMIN_KEY) {
    throw new WebError(403, "AAAAAAAAAA Spooky");
  }

  res.render('report.html', {
    session: req.session,
  });
});


router.post('/report', async (req, res) => {
  if (req.headers['sneaky-key'] != process.env.REPORT_KEY) {
    throw new WebError(403, "AAAAA Spooky");
  }

  const ip = req.headers['x-forwarded-for'] || req.connection.remoteAddress;

  const reports = path.join(process.env.REPORTS_PATH || '/reports', md5(ip));

  if (req.session.bad_apple) {
    throw new WebError(403, "Bad Apple!");
  }

  await fs.promises.writeFile(reports, JSON.stringify({
    url: req.headers['host'] + req.body.report_path,
    session: req.session,
  }));

  res.send('Report sent!');
});

router.use((req, _, next) => {
  if (req.headers['admin-key'] != process.env.ADMIN_KEY) {
    throw new WebError(400, "No!");
  }

  return next();
});

router.use('/adminlist', express.static('/admin'), serveIndex('/admin'));

router.use((err, _, res, __) => {
  if (err.code) {
    res.status(err.code).send(err.message);
  } else {
    res.status(500).send(err.message);
  }
});

module.exports = router;