// theme-toggle.js
// Adds a light/dark mode toggle that persists the user's choice in localStorage.

const THEME_STORAGE_KEY = 'preferred-theme';
const DEFAULT_THEME = 'light';

function getStoredTheme() {
  return localStorage.getItem(THEME_STORAGE_KEY);
}

function setStoredTheme(theme) {
  localStorage.setItem(THEME_STORAGE_KEY, theme);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-bs-theme', theme);
  const toggleButton = document.getElementById('themeToggle');
  const icon = toggleButton ? toggleButton.querySelector('i') : null;
  console.log('theme applied:', theme);

  if (toggleButton) {
    toggleButton.textContent = theme == 'light' ? '🌙 Dark mode' : '☀️ Light mode';
  }
}

function initThemeToggle() {
  const savedTheme = getStoredTheme();
  const startingTheme = savedTheme ? savedTheme : DEFAULT_THEME;
  applyTheme(startingTheme);

  const toggleButton = document.getElementById('themeToggle');
  if (!toggleButton) return;

  toggleButton.addEventListener('click', function () {
    const current = document.documentElement.getAttribute('data-bs-theme');
    const next = current == 'light' ? 'dark' : 'light';
    applyTheme(next);
    setStoredTheme(next);
  });
}

document.addEventListener('DOMContentLoaded', initThemeToggle);
