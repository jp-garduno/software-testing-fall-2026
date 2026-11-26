require('dotenv').config();

const express = require('express');
const path = require('path');
const { engine } = require('express-handlebars');
const routes = require('./routes');

const port = process.env.PORT || 3000;
const app = express();

// Configuración de handlebars
app.engine('handlebars', engine());
app.set('view engine', 'handlebars');
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, '..', 'public')));

app.use(routes);

app.listen(port, () => {
  console.log('Link: http://localhost:' + port);
});

/*
python -m pip show pre-commit
python -m pre_commit run --all-files
*/
