import js from '@eslint/js';
import globals from 'globals';
import { defineConfig } from 'eslint/config';

export default defineConfig([
  {
    ignores: ['node_modules/**', 'public/**'],
  },
  {
    files: ['**/*.js'],
    plugins: { js },
    extends: ['js/recommended'],
    languageOptions: {
      globals: globals.node,
    },
  },
  {
    // carga en el navegador
    files: ['**/*.js'],
    languageOptions: {
      globals: globals.browser,
    },
  },
]);

// import js from "@eslint/js";
// import globals from "globals";
// import { defineConfig } from "eslint/config";

// export default defineConfig([
//   { files: ["**/*.{js,mjs,cjs}"],
//     plugins: { js }, extends: ["js/recommended"],
//     languageOptions: { globals: globals.browser } },
// ]);
