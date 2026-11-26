module.exports = {
  testEnvironment: 'node',
  testMatch: ['<rootDir>/tests/*.test.js'],
  collectCoverageFrom: ['src/bankingSystem.js'],
  coverageReporters: ['text', 'html', 'json', 'json-summary'],
  coverageThreshold: { global: { branches: 80, functions: 80, lines: 80, statements: 80 } },
};
