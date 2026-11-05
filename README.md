# Dr. Carmelo Cedeño De la Rosa — Sitio institucional

Sitio web profesional y adaptable a móviles, construido con HTML, CSS y JavaScript, alojado en GitHub y preparado para publicarse en **Cloudflare Workers Static Assets**.

## Publicación en Cloudflare Workers

Este repositorio está configurado con `wrangler.jsonc` y los archivos públicos están organizados dentro de `public/`.

Configurar Workers Builds con:
- GitHub: `chichoarq1212/dr-carmelo-cedeno`
- Rama de producción: `main`
- Comando de compilación: ninguno
- Comando de implementación: `npx wrangler deploy`
- Directorio raíz del repositorio: `/`

Wrangler detecta la configuración del repositorio, publica el contenido de `public/` y puede desplegar nuevos cambios cuando se actualiza `main`.

## Contenido

- `public/index.html`: sitio institucional y sus ocho secciones.
- `public/assets/css/styles.css`: diseño responsive azul marino y dorado.
- `public/assets/js/app.js`: navegación, menú móvil, búsqueda, filtros y contacto.
- `public/assets/img/logo-carmelo-github.webp`: emblema institucional del Dr. Carmelo Cedeño.
- `public/assets/img/favicon.svg`: icono de navegador.
- `wrangler.jsonc`: configuración de Cloudflare Workers.

Los archivos equivalentes en la raíz original se conservan como copia de trabajo. El sitio que publica Workers es el contenido de `public/`.

## Consideraciones

El formulario de contacto prepara un correo para `info@carmelocedeno.us`; no envía ni almacena datos en un servidor. Parte de las fotos y los emblemas de otras organizaciones continúan enlazados al Google Sites original y requieren que ese sitio mantenga sus imágenes públicas.

No se inventaron reconocimientos o publicaciones; los apartados sin registros verificables se presentan como archivos en actualización.
