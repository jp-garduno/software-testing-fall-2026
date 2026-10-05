const { casesFor, runCase } = require('./shared');
// DT01 onward: all transfer, fee, and bill decision rules.
test.each(casesFor('DT'))('$id: $name', runCase);
