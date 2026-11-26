const fs = require("fs");
const path = require("path");
const {
    validarCSV,
    validarCustomerJSON,
    validarWorkflowsJSON,
} = require("./validateTestData");

const errores = [];
const rutaDatos = __dirname;
const archivosCSV = ["orderCalculations.csv", "100PruebasAlAzar.csv"]
    .filter((archivo) => fs.existsSync(path.join(rutaDatos, archivo)));

for (const archivo of archivosCSV)
    errores.push(...validarCSV(path.join(rutaDatos, archivo)));
errores.push(...validarCustomerJSON(path.join(rutaDatos, "customerValidation.json")));
errores.push(...validarWorkflowsJSON(path.join(rutaDatos, "orderWorkflows.json")));

if (errores.length > 0) {
    console.error(`Se encontraron ${errores.length} problema(s) en los datos:`);
    for (const error of errores)
        console.error(`- ${error}`);
    process.exitCode = 1;
} else {
    console.log("Archivos de datos válidos.");
}
