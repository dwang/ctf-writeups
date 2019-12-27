const path = require('path');

const express = require('express');
const nunjucks = require('nunjucks');
const morgan = require('morgan');
const session = require('express-session');
const FileStore = require('session-file-store')(session);
const bodyParser = require('body-parser');

const admin = require('./admin');
const spooky = require('./spooky');

const app = express({
  'views': path.join(__dirname, 'views'),
});

nunjucks.configure('views', {
  autoescape: true,
  express: app,
});

app.set('view engine', 'html');

app.use(session({
  resave: true,
  saveUninitialized: true,
  store: new FileStore({
    // path: '/temp' // people are complaing about sessions being dropped, but i can't understand why...
  }),
  secret: process.env.SESSION_SECRET_KEY,
}));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(morgan('combined'));

app.use('/health', (_, res) => { res.send("healthy"); });
app.use('/', express.static('.')); // We need to serve favicon.ico somehow
app.get('/', (_, res) => {
  res.render('index.html');
});

app.use('/admin', admin);
app.use('/spooky', spooky);


app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).send('Internal Server Error');
})

app.listen(8000, console.log("App listening on port 8000!"))
