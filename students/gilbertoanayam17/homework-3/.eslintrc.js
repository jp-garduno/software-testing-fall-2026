module.exports = {
  root: true,
  env: {
    node: true,
    es2022: true,
  },
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'script',
  },
  extends: ['eslint:recommended'],
  rules: {
    // Correctness
    eqeqeq: ['error', 'always'],
    'no-var': 'error',
    'prefer-const': 'error',
    'no-shadow': 'error',
    'no-return-await': 'error',

    // Readability. `curly` is enforced because a brace-less `if` is the
    // classic place for a second statement to be added later by mistake.
    curly: ['error', 'all'],
    'no-else-return': 'error',
    'prefer-template': 'error',

    // Hygiene. `no-console` is an error rather than a warning: this is a
    // library, so anything it needs to communicate should be returned or
    // thrown, never printed.
    'no-console': 'error',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
};
