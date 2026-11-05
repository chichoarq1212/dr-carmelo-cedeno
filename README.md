# Dr. Carmelo Cedeño De la Rosa — Sitio institucional

Sitio web estático profesional, adaptable a móviles y preparado para Cloudflare Workers Static Assets.

## Publicación
- Repositorio: `chichoarq1212/dr-carmelo-cedeno`
- Rama: `main`
- Comando Cloudflare: `npx wrangler deploy`
- Directorio de assets: `./public`

## Estructura
- `public/index.html`: página principal.
- `public/assets/css/styles.css`: diseño responsive.
- `public/assets/js/app.js`: menú, búsqueda, filtros, acordeones y contacto.
- `public/assets/img/carmelo-portrait.webp`: fotografía original del Dr. Carmelo, optimizada sin alterar sus rasgos.
- `public/assets/img/logo-carmelo-github.webp`: emblema institucional.
- `wrangler.jsonc`: configuración de Cloudflare Workers.

## Galería de organizaciones
Se conservaron las 16 denominaciones del directorio del sitio biográfico. Se reutilizan las imágenes enlazadas en la versión original y se incorporan emblemas de fuentes institucionales cuando se pudo verificar un recurso público. Para organizaciones sin imagen verificable se presenta su nombre completo como identificación tipográfica, sin inventar un logo.

## Interacciones
- Menú móvil y navegación activa.
- Buscador interno.
- Acordeones de formación.
- Filtros por tipo de organización.
- Pestañas y años en publicaciones.
- Formulario que prepara un correo a `info@carmelocedeno.us`; no almacena datos.

Parte de los logotipos se sirven desde los dominios oficiales de las organizaciones y las tres imágenes recuperadas de Google Sites. Si esos servicios cambian sus rutas o bloquean la carga externa, el sitio muestra el nombre completo como respaldo.
