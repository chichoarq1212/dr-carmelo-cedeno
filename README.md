# Dr. Carmelo Cedeño De la Rosa — Sitio institucional

Sitio web estático desarrollado con HTML, CSS y JavaScript. No requiere Node.js ni proceso de compilación.

## Estructura

- `index.html`: página principal y ocho secciones institucionales.
- `assets/css/styles.css`: diseño adaptable a escritorio, tablet y móvil.
- `assets/js/app.js`: menú móvil, búsqueda, navegación activa, filtros y formulario de contacto.
- `assets/img/logo-carmelo-github.webp`: emblema oficial proporcionado para el proyecto.
- `assets/img/favicon.svg`: icono del sitio.

## Publicar en Cloudflare Pages desde GitHub

1. En Cloudflare, abra **Workers & Pages**.
2. Seleccione **Create application → Pages → Connect to Git**.
3. Autorice GitHub y elija `chichoarq1212/dr-carmelo-cedeno`.
4. Configure **Framework preset: None**.
5. Deje **Build command** vacío.
6. Use `.` como **Build output directory**.
7. Guarde y despliegue.

Cada nuevo commit en la rama `main` activará una nueva publicación automática.

## Interacciones

- Menú adaptable a móvil.
- Navegación con sección activa.
- Buscador interno.
- Acordeones de formación.
- Filtros de publicaciones por categoría y año.
- Formulario que prepara un correo dirigido a `info@carmelocedeno.us`; no almacena ni envía datos a un servidor.

## Contenido y medios

Se han conservado los datos de contacto y las secciones del sitio de referencia. No se inventaron publicaciones, premios, fechas de eventos ni reconocimientos. Las áreas que no cuentan con registros verificables se presentan como archivos en actualización.

El emblema oficial está incluido en el repositorio. La fotografía del perfil y algunos logotipos de organizaciones siguen enlazados desde el sitio público original de Google Sites; conviene incorporarlos también a `assets/img` cuando se disponga de sus archivos originales autorizados para independizar completamente el sitio.

## Edición

- Contenido y enlaces: `index.html`
- Colores, tipografía y distribución: `assets/css/styles.css`
- Interacciones: `assets/js/app.js`
