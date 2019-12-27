const express = require('express');
const router = express.Router();

class WebError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

router.get('/login', (req, res) => {
  if (req.query.inject) {
    req.session.inject = req.query.inject;
  }
  if (req.query.next) {
    return res.redirect(req.query.next);
  }
  if (req.session.logged_in) {
    const redirect = req.query.next || '/spooky';

    req.session.redirect = redirect;

    return res.redirect(redirect);
  }

  res.render('spooky_login.html');
});

router.post('/login', (req, res) => {
  if (req.body.username == "10xxer" && req.body.password == "remember_not_to_hard_code_passwords_folks") {
    req.session.logged_in = true;
    res.send('Here just take it');
  } else {
    throw new WebError(403, "Too enterprise?");
  }
});

router.use((req, res, next) => {

  if (!req.session.logged_in) {
    return res.redirect(req.session.redirect || '/spooky/login');
  }

  return next();
});

router.get('/panel', (req, res) => {
  return res.render('panel.html');
});

router.use((err, _, res, __) => {
  console.error(err);
  res.status(err.code).send(err.message);
});

module.exports = router;