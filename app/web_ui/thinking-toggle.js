/* Local Bonsai UI addition. This control overrides only thinking for chat requests. */
(() => {
  const key = 'Bonsai.thinking';
  function initial() {
    try {
      const saved = localStorage.getItem(key);
      if (saved !== null) return saved === 'true';
      const config = JSON.parse(localStorage.getItem('LlamaUi.config') || '{}');
      const custom = JSON.parse(config.customJson || '{}');
      return custom.chat_template_kwargs?.enable_thinking ?? true;
    } catch { return true; }
  }
  let enabled = initial();
  const originalFetch = window.fetch.bind(window);
  window.fetch = (input, options) => {
    const url = new URL(input instanceof Request ? input.url : input, location.href);
    if (url.origin === location.origin && url.pathname === '/v1/chat/completions'
        && typeof options?.body === 'string') {
      const body = JSON.parse(options.body);
      body.chat_template_kwargs = {...body.chat_template_kwargs, enable_thinking: enabled};
      body.reasoning_control = true;
      if (!enabled) body.thinking_budget_tokens = -1;
      options = {...options, body: JSON.stringify(body)};
    }
    return originalFetch(input, options);
  };
  document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = `
      #bonsai-thinking-bar {margin:4px 0;padding:0;color:inherit;font:14px inherit;}
      #bonsai-thinking-bar label {display:flex;align-items:center;gap:9px;cursor:pointer;
        padding:9px 10px;border-radius:6px;font-size:14px;font-weight:500;}
      #bonsai-thinking-bar label:hover {background:color-mix(in srgb,currentColor 6%,transparent);}
      #bonsai-thinking-bar input {width:16px;height:16px;margin:0;accent-color:var(--foreground,#334155);}
      #bonsai-thinking-bar small {display:block;margin:0 10px 7px 35px;font-size:11px;opacity:.65;}
    `;
    document.head.append(style);
    const bar = document.createElement('div');
    bar.id = 'bonsai-thinking-bar';
    bar.innerHTML = '<label><input type="checkbox" id="bonsai-thinking">Activar thinking</label>'
      + '<small id="bonsai-thinking-status" aria-live="polite"></small>';
    // The existing sidebar is recreated when collapsed or expanded.
    const mount = () => {
      const sidebar = document.querySelector('aside.is-expanded');
      const settings = sidebar?.querySelector('a[href="#/settings/general"]');
      if (settings) {
        const row = settings.parentElement;
        if (row.nextElementSibling !== bar) row.after(bar);
      } else if (bar.isConnected) bar.remove();
    };
    new MutationObserver(mount).observe(document.body, {childList:true,subtree:true});
    mount();
    const box = bar.querySelector('input');
    const status = bar.querySelector('small');
    const render = () => {
      box.checked = enabled;
      status.textContent = enabled ? 'Razonamiento activado' : 'Respuesta directa';
    };
    box.addEventListener('change', () => {
      enabled = box.checked;
      try { localStorage.setItem(key, String(enabled)); } catch { /* Session-only if storage is unavailable. */ }
      render();
    });
    window.addEventListener('storage', event => {
      if (event.key === key) { enabled = initial(); render(); }
    });
    render();
  });
})();
