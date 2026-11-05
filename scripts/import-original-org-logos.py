#!/usr/bin/env python3
"""Copy the original organization logo images from the Dr. Carmelo Google Site.

The original image files are downloaded as-is; no logo is redrawn or recolored.
Only transparent outer padding is trimmed. Local lossless WebP copies are stored
in public/assets/org-logos/ and the Worker ID map is refreshed from the source.
"""
from __future__ import annotations

import base64
import re
import sys
from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin

import cairosvg
from PIL import Image, ImageOps
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WORKER_PATH = ROOT / "src/index.js"
WORKER = WORKER_PATH.read_text(encoding="utf-8")
HTML = (ROOT / "public/index.html").read_text(encoding="utf-8")
DEST = ROOT / "public/assets/org-logos"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

source_match = re.search(r'const SOURCE_PAGE\s*=\s*"([^"]+)"', WORKER)
logo_block = re.search(r"const LOGOS\s*=\s*\{(.*?)\};", WORKER, re.S)
if not source_match or not logo_block:
    raise SystemExit("No se pudo leer la página original o el mapa de logos del Worker.")
ORG_PAGE = source_match.group(1)
BIOGRAPHY_PAGE = "https://sites.google.com/view/drcarmelocedeno/biograf%C3%ADa?pli=1&authuser=0"
LOGOS = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', logo_block.group(1)))

targets = {}
for tag in re.findall(r"<img\b[^>]*data-org-logo[^>]*>", HTML, re.I | re.S):
    src = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.I)
    alt = re.search(r'\balt=["\']([^"\']+)["\']', tag, re.I)
    if src and alt:
        slug = src.group(1).rstrip("/").split("/")[-1]
        targets[slug] = alt.group(1)

if len(LOGOS) != 15 or len(targets) != 15:
    raise SystemExit(
        f"Se esperaban 15 organizaciones; mapa={len(LOGOS)}, tarjetas={len(targets)}."
    )

def normalize(value: str) -> set[str]:
    words = re.findall(r"[a-z0-9áéíóúñ]+", value.lower())
    ignored = {"logotipo", "logo", "original", "de", "del", "la", "el", "y", "por", "para", "con"}
    return {word for word in words if word not in ignored and len(word) > 2}

def srcset_urls(srcset: str) -> list[str]:
    candidates = []
    for part in srcset.split(","):
        bits = part.strip().split()
        if not bits:
            continue
        width = 0
        if len(bits) > 1:
            match = re.match(r"(\d+)(w|x)", bits[1])
            if match:
                width = int(match.group(1))
        candidates.append((width, bits[0]))
    return [url for _, url in sorted(candidates, reverse=True)]

def collect_images(page):
    records = []
    for frame in page.frames:
        try:
            rows = frame.locator("img").evaluate_all(
                """els => els.map(img => {
                    let node = img;
                    const context = [];
                    for (let i = 0; i < 4 && node; i++, node = node.parentElement) {
                        const value = (node.innerText || node.textContent || '').trim();
                        context.push(value.slice(0, 500));
                    }
                    return {
                        src: img.currentSrc || img.src || '',
                        rawSrc: img.getAttribute('src') || '',
                        srcset: img.getAttribute('srcset') || '',
                        dataSrc: img.getAttribute('data-src') || '',
                        alt: img.getAttribute('alt') || '',
                        width: img.naturalWidth || img.width || 0,
                        height: img.naturalHeight || img.height || 0,
                        context,
                        outer: img.outerHTML || ''
                    };
                })"""
            )
            for row in rows:
                row["frame_url"] = frame.url
                records.append(row)
        except Exception:
            continue
    return records

def collect_org_links(page):
    try:
        links = page.locator("a").evaluate_all(
            """els => els.map(a => ({
                href: a.href || '',
                text: (a.innerText || a.getAttribute('aria-label') || '').trim()
            }))"""
        )
    except Exception:
        return []
    return [
        item["href"] for item in links
        if item.get("href") and "#" not in item["href"] and (
            "organiz" in (item.get("href", "") + " " + item.get("text", "")).lower()
            or "participación" in (item.get("href", "") + " " + item.get("text", "")).lower()
        )
    ]

def image_bytes(page, record, image_id):
    candidates = []
    for value in (record.get("src"), record.get("rawSrc"), record.get("dataSrc")):
        if value:
            candidates.append(urljoin(page.url, value))
    candidates.extend(urljoin(page.url, value) for value in srcset_urls(record.get("srcset", "")))
    candidates.extend([
        f"https://sites.google.com/sitesv-images-rt/{image_id}=w1600",
        f"https://sites.google.com/sitesv-images-rt/{image_id}=w1280",
        f"https://lh7-rt.googleusercontent.com/rd-sitesv-images-rt/{image_id}=w1600",
        f"https://lh7-rt.googleusercontent.com/rd-sitesv-images-rt/{image_id}",
    ])

    seen = set()
    for url in candidates:
        if not url or url in seen or url.startswith("blob:"):
            continue
        seen.add(url)
        if url.startswith("data:image/"):
            try:
                header, payload = url.split(",", 1)
                return base64.b64decode(payload), header
            except Exception:
                continue
        try:
            response = page.request.get(
                url,
                timeout=60000,
                headers={
                    "Referer": ORG_PAGE,
                    "User-Agent": USER_AGENT,
                    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                },
            )
            if response.ok:
                content_type = response.headers.get("content-type", "")
                data = response.body()
                if data and content_type.lower().startswith("image/"):
                    return data, content_type
        except Exception:
            continue
    return None, None

def save_lossless_webp(data: bytes, content_type: str, destination: Path):
    if "svg" in content_type.lower() or data.lstrip().startswith(b"<svg"):
        data = cairosvg.svg2png(bytestring=data)
    image = Image.open(BytesIO(data))
    image.seek(0)
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA"):
        alpha = image.getchannel("A")
        bounds = alpha.getbbox()
        if bounds:
            image = image.crop(bounds)
        image = image.convert("RGBA")
    elif image.mode == "P" and "transparency" in image.info:
        image = image.convert("RGBA")
    else:
        image = image.convert("RGB")
    if image.width < 24 or image.height < 24:
        raise ValueError(f"Logo demasiado pequeño: {image.width}x{image.height}")
    image.save(destination, "WEBP", lossless=True, method=6)
    return image.size

DEST.mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=USER_AGENT,
        viewport={"width": 1440, "height": 1000},
        device_scale_factor=2,
        locale="es-PR",
    )
    page = context.new_page()
    records = []
    visited = set()
    pending = [ORG_PAGE, BIOGRAPHY_PAGE]

    while pending and len(visited) < 4:
        candidate = pending.pop(0)
        if candidate in visited:
            continue
        visited.add(candidate)
        try:
            response = page.goto(candidate, wait_until="domcontentloaded", timeout=90000)
            if response is None or not response.ok:
                print(f"Página no disponible: {candidate} ({response.status if response else 'sin respuesta'})")
                continue
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(2500)
            pending.extend(link for link in collect_org_links(page) if link not in visited)
            for _ in range(10):
                page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 700))")
                page.wait_for_timeout(250)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
            found = collect_images(page)
            print(
                f"Página revisada: {page.url} | título={page.title()!r} "
                f"| imágenes={len(found)}"
            )
            for record in found:
                record["page_url"] = page.url
                records.append(record)
        except Exception as error:
            print(f"No se pudo inspeccionar {candidate}: {error}")

    # Keep one record per original image URL.
    unique = []
    seen_records = set()
    for record in records:
        key = record.get("src") or record.get("rawSrc") or record.get("dataSrc")
        if key and key not in seen_records:
            seen_records.add(key)
            unique.append(record)
    records = unique
    print(f"Total de imágenes originales inspeccionadas: {len(records)}")

    used_sources = set()
    matched_ids = {}
    failures = []

    for slug, image_id in LOGOS.items():
        target_alt = targets.get(slug, slug.replace("-", " "))
        target_words = normalize(target_alt)
        matched = None

        # Exact original Google Sites image ID: this is the authoritative match.
        for record in records:
            combined = " ".join([
                record.get("src", ""),
                record.get("rawSrc", ""),
                record.get("dataSrc", ""),
                record.get("srcset", ""),
                record.get("outer", ""),
            ])
            if image_id in combined:
                matched = record
                break

        ranked = []
        for record in records:
            source = record.get("src") or record.get("rawSrc") or record.get("dataSrc")
            if not source or source in used_sources:
                continue
            context_values = [record.get("alt", "")] + [
                value for value in record.get("context", [])
                if value and len(value) <= 250
            ]
            score = max(
                (len(target_words & normalize(value)) / max(1, len(target_words))
                 for value in context_values),
                default=0,
            )
            if score:
                ranked.append((score, record))
        ranked.sort(key=lambda item: item[0], reverse=True)
        if matched is None and ranked and ranked[0][0] >= 0.35:
            tied = [
                item for item in ranked
                if abs(item[0] - ranked[0][0]) < 0.08
            ]
            matched = ranked[0][1] if len(tied) == 1 else None
        elif matched is None:
            matched = None

        # Last-resort ordering: the original directory places the 15 logo images
        # consecutively after the page header/social icons. Use only when exactly
        # 15 Google Sites image assets remain in the original directory page.
        if matched is None:
            org_page_records = [
                record for record in records
                if record.get("page_url", "").split("#")[0] == ORG_PAGE
                and "sites.google.com/sitesv-images-rt/" in (
                    record.get("src") or record.get("rawSrc") or ""
                )
                and int(record.get("width") or 0) >= 24
                and int(record.get("height") or 0) >= 24
            ]
            if len(org_page_records) == 15:
                matched = org_page_records[list(LOGOS).index(slug)]

        if matched is None:
            failures.append(f"{slug}: no se encontró imagen asociada a {target_alt}")
            continue

        source = matched.get("src") or matched.get("rawSrc") or matched.get("dataSrc") or ""
        id_match = re.search(r"sitesv-images-rt/([^=?]+)", source)
        image_id = id_match.group(1) if id_match else ""
        if not image_id:
            failures.append(f"{slug}: no se pudo extraer el ID de la imagen original ({source})")
            continue

        data, content_type = image_bytes(page, matched, image_id)
        if not data:
            failures.append(f"{slug}: no se pudo descargar el archivo original ({source})")
            continue

        destination = DEST / f"{slug}.webp"
        try:
            dimensions = save_lossless_webp(data, content_type or "image/*", destination)
            used_sources.add(source)
            matched_ids[slug] = image_id
            print(
                f"OK {slug}: {dimensions[0]}x{dimensions[1]} "
                f"({destination.stat().st_size} bytes) | contexto={matched.get('context', [])[:3]}"
            )
        except Exception as error:
            failures.append(f"{slug}: {error}")

    if failures:
        print("Imágenes detectadas para diagnóstico:", file=sys.stderr)
        for index, record in enumerate(records):
            print(
                f"IMG {index}: SRC={record.get('src') or record.get('rawSrc')!r} "
                f"ALT={record.get('alt')!r} CONTEXTO={record.get('context', [])[:4]!r}",
                file=sys.stderr,
            )
        browser.close()
        for failure in failures:
            print("ERROR:", failure, file=sys.stderr)
        raise SystemExit(f"No se completó la copia de los 15 logos ({len(failures)} pendientes).")

    # Refresh the Worker fallback IDs with the exact source-page IDs.
    new_lines = ["const LOGOS = {"]
    for slug in LOGOS:
        new_lines.append(f'  "{slug}": "{matched_ids[slug]}",')
    new_lines.append("};")
    new_block = "\n".join(new_lines)
    WORKER = re.sub(r"const LOGOS\s*=\s*\{.*?\};", new_block, WORKER, count=1, flags=re.S)
    WORKER_PATH.write_text(WORKER, encoding="utf-8")
    browser.close()

print(f"LISTO: se copiaron los 15 logotipos originales a {DEST} y se actualizaron sus IDs.")
