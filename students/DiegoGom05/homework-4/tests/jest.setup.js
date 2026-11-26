// jest.setup.js

// Silencia logs de consola durante la ejecución de pruebas para mantener la terminal limpia
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};
