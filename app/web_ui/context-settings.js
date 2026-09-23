/* El contexto es un ajuste del servidor; se aplica al volver a abrir la app. */
(() => {
  document.addEventListener('DOMContentLoaded', () => {
    const panel = document.createElement('section');
    panel.id = 'bonsai-context-settings';
    panel.style.cssText = 'margin:0 0 24px;padding:16px;border:1px solid #8886;border-radius:8px';
    panel.innerHTML = `<label for="bonsai-context"><strong>Tamaño del contexto (tokens)</strong></label>
      <input id="bonsai-context" type="number" min="2048" max="262144" step="1"
        style="display:block;width:100%;margin:10px 0;padding:10px;border:1px solid #8888;border-radius:6px;background:transparent;color:inherit">
      <p style="font-size:13px;opacity:.8">Incluye instrucciones, historial, resultados web, razonamiento y respuesta. Más contexto consume más memoria; no garantiza que quepa en tu GPU.</p>
      <button type="button" style="margin:12px 0;padding:8px 12px;border:1px solid #8888;border-radius:6px">Guardar contexto para el próximo inicio</button>
      <p role="status" style="font-size:13px"></p>`;
    const input = panel.querySelector('input');
    const button = panel.querySelector('button');
    const status = panel.querySelector('[role="status"]');
    async function request(value) {
      const session = window.bonsaiSession;
      if (!session) throw new Error('Cierra y vuelve a abrir la app para habilitar este ajuste.');
      const body = {token:session.token, id:'context-settings', event:'context'};
      if (value !== undefined) body.context = value;
      const response = await fetch(session.url, {method:'POST', headers:{'Content-Type':'text/plain'}, body:JSON.stringify(body)});
      if (!response.ok) throw new Error('No se pudo guardar o consultar el contexto.');
      const data = await response.json();
      input.value = data.saved;
      status.textContent = `Activo: ${data.active} tokens. Guardado: ${data.saved} tokens.`
        + (data.active !== data.saved ? ' Para aplicarlo, cierra todas las pestañas de la app, espera a que termine el modelo y vuelve a abrir el acceso directo. Recargar la página no basta.' : '');
    }
    button.onclick = async () => {
      if (!input.reportValidity() || !input.value) return;
      button.disabled = true;
      try { await request(Number(input.value)); }
      catch (error) { status.textContent = error.message; }
      finally { button.disabled = false; }
    };
    const mount = () => {
      if (!location.hash.includes('/settings/sampling-penalties')) {
        if (panel.isConnected) panel.remove();
        return;
      }
      if (panel.isConnected) return;
      const label = [...document.querySelectorAll('label')].find(el => /^(Max tokens|Máximo de tokens de salida)$/.test(el.textContent.trim()));
      if (!label) return;
      label.parentElement.before(panel);
      request().catch(error => { status.textContent = error.message; });
    };
    new MutationObserver(mount).observe(document.body, {childList:true, subtree:true});
    addEventListener('hashchange', mount);
    mount();
  });
})();
