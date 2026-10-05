const express = require('express');

const router = express.Router();

router.get('/', (req, res) => {
  const view_title = 'Home';
  res.render('home', { title: view_title });
});

router.get('/formulario', (req, res) => {
  const form_title = 'Formulario';
  res.render('formulario', { title: form_title });
});

router.get('/contador', (req, res) => {
  const contador_title = 'Contador';
  res.render('contador', { title: contador_title });
});

module.exports = router;
