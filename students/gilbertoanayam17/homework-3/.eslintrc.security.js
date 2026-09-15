// Security linting, kept separate from the default configuration because it
// needs `eslint-plugin-security`, which only exists after `npm install`.
//
// Run it with `npm run lint:security`. The pre-commit hook also runs it, using
// its own isolated environment where the plugin is installed automatically.

module.exports = {
  root: true,
  extends: ['./.eslintrc.js', 'plugin:security/recommended-legacy'],
  plugins: ['security'],
};
