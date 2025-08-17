// ---------- Utilities ----------
export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
export const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
export const fmtCurrency = (n, currency = 'USD') => new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(n);
export const fmtNumber = (n, digits=0) => new Intl.NumberFormat('en-US', { maximumFractionDigits: digits, minimumFractionDigits: digits }).format(n);
export const sum = arr => arr.reduce((a,b)=>a+b,0);
export const debounce = (fn, ms=250) => { let t; return (...args) => { clearTimeout(t); t = setTimeout(()=>fn(...args), ms); }; };

// ---------- Query string state ----------
export const parseQuery = () => Object.fromEntries(new URL(location.href).searchParams.entries());
export const toQuery = (obj) => {
  const sp = new URLSearchParams();
  Object.entries(obj).forEach(([k,v]) => { if (v !== undefined && v !== null && v !== '') sp.set(k, v); });
  return `?${sp.toString()}`;
};
export const replaceQuery = (obj) => {
  const q = toQuery(obj);
  history.replaceState(null, '', q);
};

// Binds inputs in a form to URL query string keys (name attribute) and calls onChange() debounced
export function bindFormToQuery(formEl, onChange, {debounceMs=250}={}) {
  const deb = debounce(onChange, debounceMs);
  const params = parseQuery();
  $$('input,select,textarea', formEl).forEach(el => {
    const name = el.name || el.id;
    if (!name) return;
    if (params[name] != null) {
      if (el.type === 'checkbox') el.checked = params[name] === 'true' || params[name] === '1';
      else el.value = params[name];
    }
    el.addEventListener('input', () => {
      const state = readForm(formEl);
      replaceQuery(state);
      deb(state);
    });
    el.addEventListener('change', () => {
      const state = readForm(formEl);
      replaceQuery(state);
      deb(state);
    });
  });
  // Initial update
  replaceQuery(readForm(formEl));
}

export function readForm(formEl) {
  const state = {};
  $$('input,select,textarea', formEl).forEach(el => {
    const key = el.name || el.id;
    if (!key) return;
    if (el.type === 'checkbox') state[key] = el.checked ? '1' : '0';
    else state[key] = el.value;
  });
  return state;
}

// ---------- Service worker auto-register ----------
export function registerSW() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/serviceWorker.js').catch(()=>{});
    });
  }
}
registerSW();
