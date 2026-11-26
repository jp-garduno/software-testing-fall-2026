const { casesFor, runCase } = require('./shared');
// ST01 onward: public action sequences and valid/invalid state transitions.
test.each(casesFor('ST'))('$id: $name', runCase);
