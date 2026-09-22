# Componentes de terceros

La interfaz estática de `app/web_ui/` procede de llama-ui, distribuida con el fork [PrismML-Eng/llama.cpp](https://github.com/PrismML-Eng/llama.cpp/tree/9a9394a895b96003ca842a6041cb28ac49a108f7), revisión `9a9394a895b96003ca842a6041cb28ac49a108f7`.

Se conserva el aviso MIT del proyecto en `LICENSES/llama.cpp.txt` y los avisos de los componentes vendorizados de la interfaz en `LICENSES/`. Los comentarios de licencia presentes en los recursos compilados se conservan. El código fuente y las dependencias de esta versión están en `tools/ui/` del repositorio de origen.

Los cambios locales incluyen la traducción al español, el control de thinking, los ajustes visuales y el control de cierre. El archivo `chat-session.js` se genera al ejecutar la aplicación y no se distribuye.

Los pesos del modelo, el runtime y las bibliotecas CUDA no están incluidos: el paso 002 los descarga de sus distribuidores oficiales. Sus licencias y condiciones corresponden a esos distribuidores. Estos avisos no asignan una licencia nueva al código propio de este proyecto.
