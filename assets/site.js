// Persisted theme (light/dark) using a data attribute so it won't affect calculators
const THEME_KEY = 'site:theme';
const html = document.documentElement;

function applyTheme(t) {
  html.setAttribute('data-theme', t);
}
applyTheme(localStorage.getItem(THEME_KEY) || 'dark');

const btn = document.getElementById('themeToggle');
if (btn) {
  btn.addEventListener('click', () => {
    const next = (html.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });
}

// (Optional) small DOM helpers if you want them elsewhere
export const $ = (sel, root=document) => root.querySelector(sel);
export const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
