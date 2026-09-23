const { casesFor, runCase } = require('./shared');
// EP01 onward: identical partition representatives and oracles to pytest.
test.each(casesFor('EP'))('$id: $name', runCase);
