import { config } from "dotenv"
config();

import express from "express";
import path from "path";
import { engine } from "express-handlebars";

const port = process.env.PORT || 3000;
const app = express();

// Configuración de handlebars
app.engine("handlebars", engine());
app.set("view engine", "handlebars");
app.set("views", path.join(__dirname, "views"))

app.get("/", (req, res) => {
    res.render("home", { title: 'Home' });
});

app.get("/formulario", (req, res) => {
    res.render("formulario", { title: 'Formulario' });
});

app.listen(port, () => {
    console.log("http://localhost:" + port);
});