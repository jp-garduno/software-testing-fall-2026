const { casesFor, runCase } = require('./shared');
// BV01 onward: on/below/above boundary values from the design catalog.
test.each(casesFor('BV'))('$id: $name', runCase);
