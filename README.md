# Agente local Bonsai 2 27B

Scripts Python para preparar y ejecutar **Ternary-Bonsai-2-27B PTQ1_0** en Windows con NVIDIA CUDA, tanto en la consola Python de PyCharm como en una interfaz web local con Markdown, tablas y respuestas progresivas.

Python controla el proceso; la inferencia la realiza el runtime de PrismML basado en llama.cpp. El asistente conversa, pero **no ejecuta herramientas, no navega por internet y no accede automáticamente a tus archivos**.

## Así se ve la aplicación

Pantalla de inicio, con la interfaz en español y el control de razonamiento en el menú lateral:

![Pantalla de inicio del chat web de Bonsai 2](docs/imagenes/app-inicio.png)

Ejemplo de respuesta a una consulta de redacción técnica:

![Respuesta de Bonsai 2 con razonamiento activado y métricas de generación](docs/imagenes/app-respuesta.png)

Estas capturas fueron seleccionadas para mostrar la aplicación. Incluyen los títulos de conversaciones visibles, pero no se distribuye la base de datos del historial del navegador.

### Velocidad observada

Como referencia de uso, el autor reporta **alrededor de 30 tokens por segundo de generación** en su **NVIDIA RTX 4070 Laptop de 8 GB**, con Bonsai 2 27B PTQ1_0 y el runtime CUDA de PrismML, sin DSpark.

La configuración distribuida del chat web usa contexto de 8192 tokens, salida máxima de 4096, thinking activado con esfuerzo `medium`, 8 threads y offloading a GPU. La velocidad depende del contexto, la consulta, los ajustes efectivos del navegador y la carga del equipo; 30 tokens/s es una referencia aproximada, no un promedio de benchmark publicado ni una garantía para cada respuesta.

La captura de respuesta muestra **24,74 tokens/s** para esa consulta concreta. Los **225,50 tokens/s** que aparecen junto al mensaje del usuario corresponden al procesamiento de la entrada, no a la generación de la respuesta. Con thinking, el modelo puede generar tokens de razonamiento antes de mostrar texto al usuario.

## Qué contiene

| Archivo | Función |
|---|---|
| `001 - Preparar entorno.py` | Busca un entorno compatible con Python 3.12 y crea uno si hace falta. |
| `002 - Descargar modelo y runtime.py` | Descarga los recursos oficiales y comprueba tamaño y SHA256. |
| `003 - Primer llamado.py` | Hace una consulta y cierra el modelo al terminar. |
| `004 - Chat persistente.py` | Mantiene el modelo cargado para usar `agente()` en la consola Python. |
| `005 - Chat web.py` | Carga el modelo y abre la aplicación en el navegador. |
| `rutas.py` | Lee las ubicaciones privadas de cada instalación. |
| `rutas_ejemplo.json` | Plantilla vacía para configurar esas ubicaciones. |
| `app/` | Lanzador web, cierre automático, configuración e interfaz. |

No se incluyen pesos, ejecutables CUDA, entornos Python, archivos de conversaciones, resultados de pruebas ni rutas personales; solo se incluyen las capturas de demostración mostradas arriba. No hace falta instalar paquetes de Python adicionales: estos scripts utilizan la biblioteca estándar. La interfaz ya está compilada; no necesitas Node.js.

## Requisitos

- Windows de 64 bits y **Python 3.12** instalado.
- GPU NVIDIA y driver compatible con el runtime CUDA 12.4. `nvidia-smi` debe estar disponible.
- Espacio para el modelo de 5,95 GB, los ZIP del runtime y CUDA, y sus archivos extraídos. Conviene disponer de al menos 12 GB libres; el descargador comprueba espacio antes de continuar.
- Conexión a internet para la descarga inicial y un navegador moderno para el chat web.

El proyecto se desarrolló con una RTX 4070 Laptop de 8 GB. Esto no garantiza compatibilidad ni rendimiento en otras GPU. No se instalan ni modifican drivers. No se utiliza DSpark.

## 1. Descargar el proyecto y configurar las rutas

Descarga el ZIP del repositorio desde **Code → Download ZIP** y extráelo, o clónalo en una carpeta nueva. Abre esa carpeta en PyCharm.

Copia `rutas_ejemplo.json` como **`rutas_locales.json`**, al lado de los scripts, y completa las cuatro rutas. Ejemplo ficticio: sustituye `TU_USUARIO` y las carpetas por tus valores reales. En JSON puedes usar `/` para evitar escapar las barras.

```json
{
  "PATH_PROYECTO": "C:/Proyectos/AGENTE_LOCAL_BONSAI_2_27B",
  "PATH_AMBIENTES": "C:/Users/TU_USUARIO/AMBIENTES_PYTHON",
  "PATH_MODELOS": "C:/Users/TU_USUARIO/OneDrive/Proyectos/MODELOS_DESCARGADOS",
  "PATH_PYTHON": "C:/Users/TU_USUARIO/AMBIENTES_PYTHON/bonsai_27b/Scripts/python.exe"
}
```

- `PATH_PROYECTO`: carpeta que contiene los cinco scripts y `app/`.
- `PATH_AMBIENTES`: directorio externo donde buscar o crear entornos Python.
- `PATH_MODELOS`: directorio externo de pesos. **Créalo antes del paso 002.**
- `PATH_PYTHON`: intérprete del entorno elegido; debe estar dentro de `PATH_AMBIENTES`.

El archivo local está excluido de Git. No pongas pesos ni entornos dentro del proyecto. Las rutas deben ser absolutas; no se expanden variables como `%USERPROFILE%` dentro del JSON.

## 2. Preparar el entorno

Desde la terminal, situada en la carpeta del proyecto:

```bat
py -3.12 "001 - Preparar entorno.py"
```

El script busca Python 3.12 en los entornos existentes. Si no encuentra uno compatible, crea `bonsai_27b` dentro de `PATH_AMBIENTES`. No reemplaza un entorno incompatible existente.

Al terminar muestra el intérprete que debes seleccionar en **PyCharm → Python Interpreter**. Actualiza `PATH_PYTHON` en el JSON si el intérprete seleccionado difiere del que habías indicado. Reinicia la consola Python después de cambiar las rutas.

En los comandos siguientes, `python` debe ser ese intérprete: usa la terminal con el entorno activado o su ruta completa entre comillas.

## 3. Descargar modelo y runtime

```bat
python "002 - Descargar modelo y runtime.py"
```

Los pesos se guardan en `PATH_MODELOS/Ternary-Bonsai-2-27B/`. Los ejecutables quedan en `PATH_PROYECTO/runtime/`. Los archivos existentes se verifican y reutilizan; no se sobrescriben si su contenido es distinto.

La descarga verifica tamaño y SHA256 fijados en el código. Si una descarga queda incompleta, el archivo `.part` se conserva y se informa el error; **no hay reanudación automática**. Revisa ese parcial antes de decidir eliminarlo y volver a descargar. No ejecutes dos descargas simultáneas.

### Recursos fijados

| Recurso | Versión |
|---|---|
| Modelo | [prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf), revisión `6ed5e12bf84b7a63069882c91dd9e9218647d17b` |
| Archivo | `Ternary-Bonsai-2-27B-PTQ1_0.gguf`, 5.946.648.928 bytes |
| SHA256 del modelo | `53107f530aa52eb00912263ab1ee29bd199261c87cd7b4ad4ca1318c1fe33ee3` |
| Runtime | [PrismML llama.cpp prism-b10709-9a9394a](https://github.com/PrismML-Eng/llama.cpp/releases/tag/prism-b10709-9a9394a), Windows x64 CUDA 12.4 |
| Bibliotecas CUDA | [llama.cpp b10964](https://github.com/ggml-org/llama.cpp/releases/tag/b10964), paquete CUDA 12.4 |

Esta distribución usa **Bonsai 2 ternario PTQ1_0**, no Bonsai 1 Q1_0. No sustituyas el runtime por otro sin comprobar que admite este formato.

## 4. Primera consulta

Edita `pregunta` y los parámetros visibles del `003`, y ejecútalo:

```bat
python "003 - Primer llamado.py"
```

El modelo se carga para esa consulta y se cierra al terminar. Se muestran la respuesta, el tiempo total y las métricas disponibles. La respuesta y el registro técnico se guardan en `privado/consultas_terminal/`, excluido de Git.

## 5. Abrir el chat web

Cierra cualquier otra instancia del modelo y ejecuta:

```bat
python "005 - Chat web.py"
```

Al terminar la carga se abre **http://127.0.0.1:8088/** en el navegador predeterminado. Si no se abre automáticamente, visita esa dirección.

También puedes llamarlo desde la consola Python de PyCharm, con la raíz del proyecto como directorio de trabajo:

```python
import runpy
from rutas import PATH_PROYECTO

runpy.run_path(str(PATH_PROYECTO / "005 - Chat web.py"))
```

La llamada permanece activa mientras funciona la web. Puedes cambiar `contexto`, `max_tokens`, `thinking`, `esfuerzo` y `puerto` en el `005`. Los valores iniciales son contexto 8192, salida máxima 4096, thinking activado y esfuerzo `medium`.

En el menú lateral puedes activar o desactivar thinking. Los ajustes guardados en el navegador pueden prevalecer sobre los valores iniciales del script. El límite de salida incluye el razonamiento y la respuesta visible; además, entrada + historial + generación deben caber en el contexto total.

La aplicación escucha solo en localhost. No está preparada para exponerse a internet.

### Cerrar y liberar memoria

Cerrar la última pestaña del chat activa el cierre del modelo tras unos 8 segundos. Si hay más pestañas del chat abiertas, la sesión continúa. Si el navegador termina abruptamente, la detección puede tardar unos 3 minutos; una pestaña suspendida también puede caducar.

Evita forzar la terminación de Python: puede dejar un proceso del runtime abierto. Cierra primero las pestañas y espera a que aparezca «Servidor detenido».

## Alternativa: conversar y calcular en la consola Python

El `004` está pensado para una **consola Python persistente**, no para un proceso que termina inmediatamente. Con la raíz del proyecto como directorio de trabajo:

```python
from rutas import PATH_PROYECTO

exec((PATH_PROYECTO / "004 - Chat persistente.py").read_text(encoding="utf-8"))

agente()  # Aparece «Tú:»; escribe la pregunta sin comillas y pulsa Enter.
total = 500 * 1.19
agente(f"Explica este resultado: {total}")
respuesta = agente("Resume nuestra conversación", mostrar=False)
limpiar_historial()
cerrar_modelo()
```

La respuesta aparece progresivamente. Tus variables no se comparten automáticamente: inclúyelas en el texto si quieres que el modelo las conozca. Cierra el modelo del `004` antes de abrir la web. El `004` usa el puerto 8090.

## Privacidad y almacenamiento

- El repositorio es una copia seleccionada del código, no una sincronización del directorio privado de desarrollo.
- Los chats web se guardan en el almacenamiento del navegador. Cambiar de navegador, perfil o puerto puede mostrar un historial distinto.
- `app/datos/registros/` contiene registros técnicos de ejecución; está excluido de Git.
- `app/web_ui/chat-session.js` se genera al iniciar y no se versiona.
- No se incluyen archivos de conversaciones, registros de uso, rutas personales, archivos `.env`, pesos, runtime ni entornos. Las dos capturas de demostración sí muestran el contenido y los títulos visibles seleccionados por el autor.
- Guarda las exportaciones de conversaciones fuera del repositorio o en `privado/`. Revisa los archivos antes de cualquier commit; no uses `git add -f` para datos privados.

Un `.gitignore` no borra contenido ya versionado ni protege un archivo privado colocado manualmente dentro de una ruta permitida. Este repositorio limita por defecto los archivos de la raíz que pueden incorporarse.

## Problemas habituales

| Mensaje o síntoma | Qué revisar |
|---|---|
| Falta `rutas_locales.json` | Copia la plantilla y completa las cuatro rutas. |
| No encuentra `rutas` | En una consola interactiva, sitúa el directorio de trabajo en la raíz del proyecto. |
| GPU ocupada | Cierra juegos u otros chats; en el 004 usa `cerrar_modelo()`. El 005 evita cargar otra copia cuando observa más de 2300 MiB usados. |
| Puerto 8088 ocupado | Revisa si ya hay una instancia web abierta. Cierra esa instancia antes de iniciar otra. |
| Solo aparece «Pensando» o una respuesta cortada | Desactiva thinking para la siguiente consulta o ajusta el máximo de salida y el contexto disponible. |
| Falta el modelo o runtime | Ejecuta el 002 y revisa las rutas. |
| No carga con CUDA | Revisa el driver NVIDIA y el registro de esa ejecución en `app/datos/registros/`. |

## Alcance y componentes de terceros

Esta entrega distribuye la aplicación y los scripts de uso. No incluye los experimentos privados ni promete una velocidad concreta. La validación de la copia de publicación comprueba código, recursos y arranque simulado; no sustituye una prueba de descarga e inferencia en cada PC.

Consulta [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) y `LICENSES/` para la procedencia y los avisos conservados de la interfaz. Los pesos y binarios se descargan por separado de sus distribuidores oficiales.
