/* Spanish UI labels only: never translate conversation content or editable values. */
(() => {
  const strings = {
    'Addon for the temperature sampler. The added value to the range of dynamic temperature, which adjusts probabilities by entropy of tokens.':'Amplía el rango de temperatura dinámica, que ajusta las probabilidades según la entropía de los tokens.',
    'Addon for the temperature sampler. Smoothes out the probability redistribution based on the most probable token.':'Suaviza la redistribución de probabilidades a partir del token más probable.',
    'XTC sampler cuts out top tokens; this parameter controls the chance of cutting tokens at all. 0 disables XTC.':'Probabilidad de que XTC descarte tokens de alta probabilidad. Usa 0 para desactivar XTC.',
    'XTC sampler cuts out top tokens; this parameter controls the token probability that is required to cut that token.':'Umbral de probabilidad a partir del cual XTC puede descartar un token.',
    'Sorts and limits tokens based on the difference between log-probability and entropy.':'Ordena y limita tokens según la diferencia entre logaritmo de probabilidad y entropía.',
    'The order at which samplers are applied, in simplified way. Default is "top_k;typ_p;top_p;min_p;temperature": top_k->typ_p->top_p->min_p->temperature':'Orden de aplicación de los métodos de muestreo. Orden simplificado predeterminado: top_k → typ_p → top_p → min_p → temperature.',
    'Limits tokens based on whether they appear in the output or not.':'Penaliza tokens según si ya aparecieron en la salida.',
    'DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the DRY sampling multiplier.':'DRY reduce repeticiones incluso con contextos largos. Este valor fija su multiplicador.',
    'DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the DRY sampling base value.':'DRY reduce repeticiones incluso con contextos largos. Este valor fija su base.',
    'DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the allowed length for DRY sampling.':'Longitud de repetición permitida antes de aplicar la penalización DRY.',
    'DRY sampling reduces repetition in generated text even across long contexts. This parameter sets DRY penalty for the last n tokens.':'Cantidad de tokens previos que DRY revisa para penalizar repeticiones.',
    'New chat':'Nuevo chat','Search':'Buscar','Settings':'Ajustes','MCP Servers':'Servidores MCP',
    'MCP servers':'Servidores MCP','Recent conversations':'Conversaciones recientes',
    'Expand navigation':'Expandir menú','Collapse navigation':'Contraer menú','Go to start':'Ir al inicio',
    'Hello there':'Hola','Type a message or upload files to get started':'Escribe un mensaje o adjunta archivos para comenzar',
    'Type a message...':'Escribe un mensaje…','Send':'Enviar','Stop':'Detener','Continue':'Continuar',
    'Copy':'Copiar','Copied!':'¡Copiado!','Edit':'Editar','Delete':'Eliminar','Cancel':'Cancelar',
    'Save':'Guardar','Close':'Cerrar','Confirm':'Confirmar','Download':'Descargar','Upload':'Subir',
    'Regenerate':'Regenerar','Fork conversation':'Crear una copia del chat','Reasoning':'Razonamiento',
    'Thinking...':'Razonando…','Toggle content':'Mostrar u ocultar contenido','Close tab':'Cerrar pestaña',
    'Scroll left':'Desplazar a la izquierda','Scroll right':'Desplazar a la derecha',
    'Context usage':'Uso del contexto','Open conversations':'Conversaciones abiertas',
    'Add files, prompts, tools or MCP Servers':'Añadir archivos, instrucciones, herramientas o servidores MCP',
    'Open command picker':'Abrir selector de comandos','Open prompt picker':'Abrir selector de instrucciones',
    'Open file mention picker':'Abrir selector de archivos','Activar thinking':'Activar razonamiento',
    'Connecting to Server':'Conectando con el servidor','Initializing connection to server...':'Iniciando conexión con el servidor…',
    'Connecting...':'Conectando…','General':'General','Display':'Apariencia','Tools':'Herramientas',
    'Agentic':'Agentes','Import/Export':'Importar y exportar','Sampling & Penalties':'Muestreo y penalizaciones',
    'Developer':'Avanzado','Save settings':'Guardar ajustes','Reset to default':'Restablecer valores predeterminados',
    'Reload app':'Recargar aplicación',"Settings are saved in browser's localStorage":'Los ajustes se guardan en este navegador',
    'Theme':'Tema','System':'Sistema','Light':'Claro','Dark':'Oscuro','API Key':'Clave de API',
    'System Message':'Mensaje del sistema','Show system message':'Mostrar mensaje del sistema',
    'Show system message in conversations':'Mostrar el mensaje del sistema en los chats',
    'Paste long text to file length':'Longitud para convertir texto pegado en archivo',
    'Send message on Enter':'Enviar al pulsar Enter','Show microphone on empty input':'Mostrar micrófono cuando no hay texto',
    'Enable "Continue" button':'Habilitar el botón «Continuar»','Conversation title':'Título del chat',
    'Use first non-empty line for the conversation title':'Usar la primera línea no vacía como título',
    'Generate title with LLM':'Generar título con el modelo','LLM title generation prompt':'Instrucción para generar el título',
    'Copy text attachments as plain text':'Copiar adjuntos de texto como texto plano',
    'Parse PDF as image':'Procesar PDF como imagen','Maximum image resolution (megapixels)':'Resolución máxima de imagen (megapíxeles)',
    'Show message generation statistics':'Mostrar estadísticas de generación',
    'Show statistics for individual agentic turns':'Mostrar estadísticas de cada paso del agente',
    'Show thought in progress':'Mostrar razonamiento durante la generación',
    'Always show tool call content':'Mostrar siempre el contenido de llamadas a herramientas',
    'Render user content as Markdown':'Mostrar mensajes del usuario con formato Markdown',
    'Render thinking as Markdown':'Mostrar razonamiento con formato Markdown',
    'Use full height code blocks':'Mostrar bloques de código con altura completa',
    'Disable automatic scroll':'Desactivar desplazamiento automático',
    'Always show sidebar on desktop':'Mantener visible el menú lateral en escritorio',
    'Conversation tabs':'Pestañas de chats','Show raw model names':'Mostrar identificadores completos del modelo',
    'Show model quantization information':'Mostrar cuantización del modelo','Show model tags':'Mostrar etiquetas del modelo',
    'Show build version information':'Mostrar versión de la aplicación','Show full path in mentions':'Mostrar ruta completa en menciones',
    'Agentic turns':'Pasos del agente','MCP request timeout (seconds)':'Tiempo límite de solicitudes MCP (segundos)',
    'Mention search depth':'Profundidad de búsqueda de menciones','Temperature':'Temperatura',
    'Dynamic temperature range':'Rango de temperatura dinámica','Dynamic temperature exponent':'Exponente de temperatura dinámica',
    'XTC probability':'Probabilidad XTC','XTC threshold':'Umbral XTC','Typical P':'P típica',
    'Max tokens':'Máximo de tokens de salida','Custom':'Personalizado','Samplers':'Métodos de muestreo',
    'Backend sampling':'Muestreo en el acelerador','Repeat last N':'Últimos N tokens para repetición',
    'Repeat penalty':'Penalización por repetición','Presence penalty':'Penalización por presencia',
    'Frequency penalty':'Penalización por frecuencia','DRY multiplier':'Multiplicador DRY',
    'DRY base':'Base DRY','DRY allowed length':'Longitud permitida de DRY','DRY penalty last N':'Últimos N tokens para DRY',
    'Pre-fill KV cache after response':'Preparar caché KV después de responder',
    'Disable reasoning content parsing':'Desactivar separación del razonamiento',
    'Exclude reasoning from context':'Excluir razonamiento del historial enviado',
    'Enable raw output toggle':'Habilitar vista de texto sin formato','JavaScript sandbox tool':'Herramienta JavaScript aislada',
    'Symbolic math (nerdamer)':'Matemática simbólica (nerdamer)','Custom JSON':'JSON personalizado','Custom CSS':'CSS personalizado',
    'Import':'Importar','Export':'Exportar','Import settings':'Importar ajustes','Export settings':'Exportar ajustes',
    'Import conversations':'Importar conversaciones','Export conversations':'Exportar conversaciones',
    'Select all':'Seleccionar todo','Deselect all':'Deseleccionar todo','No results found':'No se encontraron resultados',
    'Search conversations...':'Buscar conversaciones…','Search models...':'Buscar modelos…',
    'Choose the color theme for the interface. You can choose between System (follows your device settings), Light, or Dark.':'Elige el tema: Sistema (según tu dispositivo), Claro u Oscuro.',
    'The starting message that defines how model should behave.':'Instrucción inicial que define cómo debe comportarse el modelo.',
    'Set the API Key if you are using':'Introduce la clave de API si usas la opción',
    'option for the server.':'en el servidor.',
    'Display the system message at the top of each conversation.':'Muestra el mensaje del sistema al inicio de cada chat.',
    'On pasting long text, it will be converted to a file. You can control the file length by setting the value of this parameter. Value 0 means disable.':'Convierte textos pegados largos en archivos al superar esta longitud. Usa 0 para desactivarlo.',
    'Use Enter to send messages and Shift + Enter for new lines. When disabled, use Ctrl/Cmd + Enter.':'Enter envía el mensaje y Mayús + Enter añade una línea. Si lo desactivas, usa Ctrl/Cmd + Enter para enviar.',
    'Automatically show microphone button instead of send button when textarea is empty for models with audio modality support.':'Muestra el micrófono cuando no hay texto, si el modelo admite audio.',
    'Enable "Continue" button for assistant messages, including reasoning models.':'Permite continuar respuestas del asistente, incluso con modelos de razonamiento.',
    'Choose how conversation titles are generated. The first non-empty line uses a fast deterministic rule; the LLM option uses a model-generated title from the first message exchange.':'Elige entre usar la primera línea del chat o pedir al modelo que genere un título a partir del primer intercambio.',
    'When copying a message with text attachments, combine them into a single plain text string instead of a special format that can be pasted back as attachments.':'Al copiar mensajes con adjuntos de texto, reúne su contenido en texto plano.',
    'Parse PDF as image instead of text. Automatically falls back to text processing for non-vision models.':'Procesa el PDF como imagen. Si el modelo no admite visión, utiliza texto automáticamente.',
    'Images larger than this will be resized before sending to server. Set to 0 to disable.':'Reduce imágenes que superen este tamaño antes de enviarlas. Usa 0 para desactivarlo.',
    'Controls the randomness of the generated text by affecting the probability distribution of the output tokens. Higher = more random, lower = more focused.':'Controla la variación del texto generado: valores altos producen respuestas más variadas; valores bajos, más predecibles.',
    'The maximum number of token per output. Use -1 for infinite (no limit).':'Máximo de tokens por respuesta, incluido el razonamiento. Usa -1 para no fijar límite de salida; sigue aplicándose el límite de contexto.',
    'Keeps only k top tokens.':'Considera únicamente los K tokens más probables.',
    'Limits tokens to those that together have a cumulative probability of at least p':'Limita las opciones a los tokens cuya probabilidad acumulada alcanza P.',
    'Limits tokens based on the minimum probability for a token to be considered, relative to the probability of the most likely token.':'Descarta tokens por debajo de una probabilidad mínima relativa al token más probable.',
    'Enable backend-based samplers. When enabled, supported samplers run on the accelerator backend for faster sampling.':'Ejecuta los métodos compatibles de muestreo en el acelerador para reducir su coste.',
    'Last n tokens to consider for penalizing repetition':'Cantidad de tokens previos que se revisan para penalizar repeticiones.',
    'Controls the repetition of token sequences in the generated text':'Controla la repetición de secuencias en el texto generado.',
    'Limits tokens based on whether they appear in the output.':'Penaliza tokens que ya aparecieron en la salida.',
    'Limits tokens based on how often they appear in the output.':'Penaliza tokens según su frecuencia en la salida.',
    'After each response, re-submit the conversation to pre-fill the server KV cache. Makes the next turn faster since the prompt is already encoded while you read the response.':'Prepara la caché del historial después de responder para reducir la espera en la próxima consulta.',
    'Send reasoning_format=none so the server returns thinking tokens inline instead of extracting them into a separate field.':'Devuelve el razonamiento junto con la respuesta, sin separarlo en otro campo. No desactiva el razonamiento.',
    'Strip thinking from previous messages before sending. When off, thinking is sent back via the reasoning_content field so the model sees its own chain-of-thought across turns.':'Excluye el razonamiento de mensajes anteriores del historial enviado al modelo.',
    'Show toggle button to display messages as plain text instead of Markdown-formatted content':'Permite alternar entre texto plano y formato Markdown.',
    'Expose a run_javascript tool to the model. Code runs in a Web Worker inside a sandboxed iframe with an opaque origin, isolated from the WebUI and its API, with a hard timeout.':'Ofrece una herramienta JavaScript en un entorno aislado de la interfaz y de su API, con tiempo límite.',
    'Custom JSON parameters to send to the API. Must be valid JSON format.':'Parámetros adicionales para la API. Deben tener formato JSON válido.',
    'CSS injected into the page at runtime. Set it here, or ship it server side via the --ui-config customCss field.':'Estilos CSS adicionales para personalizar la interfaz.',
    'Display generation statistics (tokens/second, token count, duration) below each assistant message.':'Muestra velocidad, cantidad de tokens y duración debajo de cada respuesta.',
    'Expand thought process by default when generating messages.':'Despliega el razonamiento mientras se genera la respuesta.',
    'Automatically expand tool call details while executing and keep them expanded after completion.':'Muestra los detalles de llamadas a herramientas durante y después de su ejecución.',
    'Render user messages using markdown formatting in the chat. Turn this off to keep a message exactly as typed; @-mention badges show either way.':'Aplica Markdown a tus mensajes. Desactívalo para conservar el texto tal como lo escribiste.',
    'Render the reasoning/thinking block content as formatted Markdown instead of plain text.':'Aplica formato Markdown al bloque de razonamiento.',
    'Always display code blocks at their full natural height, overriding any height limits.':'Muestra completos los bloques de código, sin limitar su altura.',
    'Disable automatic scrolling while messages stream so you can control the viewport position manually.':'Permite controlar manualmente el desplazamiento mientras se genera una respuesta.',
    'Always keep the sidebar visible on desktop instead of auto-hiding it.':'Mantiene abierto el menú lateral en escritorio.',
    'Show open chats as browser-style tabs above the conversation, one per open chat. When disabled, only one chat is shown at a time.':'Muestra una pestaña por cada chat abierto. Si lo desactivas, se muestra un chat a la vez.',
    'Display the current build version in the bottom-right corner of the interface.':'Muestra la versión actual en la esquina inferior derecha.'
  };
  const translate = value => {
    const text = value.trim();
    const replacement = strings[text.replace(/\s+/g, ' ')];
    return replacement ? value.replace(text, replacement) : value;
  };
  function protectedContent(el) {
    if (el.closest('script,style,textarea,pre,code,[contenteditable="true"]')) return true;
    // Preserve user-authored messages, assistant output and conversation names.
    if (el.closest('[role="group"][aria-label$="message with actions"]') && !el.closest('button')) return true;
    if (el.closest('aside ul,aside [role="list"],nav[aria-label="Open conversations"],nav[aria-label="Conversaciones abiertas"]')) {
      if (el.closest('a[href="#/"]') || el.parentElement?.querySelector(':scope > a[href="#/"]')) return false;
      return !el.closest('button[aria-label]');
    }
    return false;
  }
  function visit(root) {
    if (root.nodeType === Node.TEXT_NODE) {
      const el = root.parentElement;
      if (el && !protectedContent(el)) {
        const translated = translate(root.data);
        if (translated !== root.data) root.data = translated;
      }
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE || root.matches('script,style,textarea,pre,code,[contenteditable="true"]')) {
      if (root.nodeType === Node.ELEMENT_NODE && root.matches('textarea')) {
        const value = root.getAttribute('placeholder');
        if (value && translate(value) !== value) root.setAttribute('placeholder', translate(value));
      }
      return;
    }
    for (const attr of protectedContent(root) ? [] : ['aria-label','title','placeholder']) {
      const value = root.getAttribute(attr);
      if (value) {
        const translated = attr === 'placeholder' && value.startsWith('Default: ') ? value.replace('Default: ', 'Predeterminado: ') : translate(value);
        if (value !== translated) root.setAttribute(attr, translated);
      }
    }
    for (const child of root.childNodes) visit(child);
  }
  document.addEventListener('DOMContentLoaded', () => {
    document.documentElement.lang = 'es';
    // Visit only mutated subtrees, not the entire conversation on every generated token.
    new MutationObserver(records => {
      for (const record of records) {
        if (record.type === 'childList') for (const node of record.addedNodes) visit(node);
        else visit(record.target);
      }
    }).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,
      attributeFilter:['aria-label','title','placeholder']});
    visit(document.body);
  });
})();
