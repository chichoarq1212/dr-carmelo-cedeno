#!/usr/bin/env python3
"""Copy the exact original organization logo images from Google Sites.

The verified Google Sites media IDs in src/index.js identify each original logo.
The files are downloaded unchanged, converted to lossless WebP, and stored locally.
"""
from __future__ import annotations

import base64
import re
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
        if slug.lower().endswith(".webp"):
            slug = slug[:-5]
        targets[slug] = alt.group(1)

if len(LOGOS) != 15 or len(targets) != 15 or set(LOGOS) != set(targets):
    raise SystemExit(
        f"El mapa y las tarjetas deben contener las mismas 15 organizaciones; "
        f"mapa={len(LOGOS)}, tarjetas={len(targets)}."
    )

def collect_images(page):
    records = []
    for frame in page.frames:
        try:
            rows = frame.locator("img").evaluate_all(
                """els => els.map(img => ({
                    src: img.currentSrc || img.src || '',
                    rawSrc: img.getAttribute('src') || '',
                    srcset: img.getAttribute('srcset') || '',
                    dataSrc: img.getAttribute('data-src') || '',
                    alt: img.getAttribute('alt') || '',
                    width: img.naturalWidth || img.width || 0,
                    height: img.naturalHeight || img.height || 0,
                    outer: img.outerHTML || ''
                }))"""
            )
            for row in rows:
                row["frame_url"] = frame.url
                records.append(row)
        except Exception:
            continue
    return records

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

def download_original(page, record):
    candidates = []
    for value in (record.get("src"), record.get("rawSrc"), record.get("dataSrc")):
        if value:
            candidates.append(urljoin(ORG_PAGE, value))
    candidates.extend(urljoin(ORG_PAGE, value) for value in srcset_urls(record.get("srcset", "")))

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
                print(f"Página no disponible: {candidate}")
                continue
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(2500)
            for _ in range(10):
                page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 700))")
                page.wait_for_timeout(250)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(500)
            found = collect_images(page)
            print(f"Página revisada: {page.url} | imágenes={len(found)}")
            for record in found:
                record["page_url"] = page.url
                records.append(record)
        except Exception as error:
            print(f"No se pudo inspeccionar {candidate}: {error}")

    # Preserve one entry per image URL.
    unique = []
    seen_urls = set()
    for record in records:
        key = record.get("src") or record.get("rawSrc") or record.get("dataSrc")
        if key and key not in seen_urls:
            seen_urls.add(key)
            unique.append(record)
    records = unique
    print(f"Imágenes originales inspeccionadas: {len(records)}")

    matched_ids = {}
    failures = []

    for slug, expected_id in LOGOS.items():
        matched = None
        for record in records:
            combined = " ".join([
                record.get("src", ""),
                record.get("rawSrc", ""),
                record.get("dataSrc", ""),
                record.get("srcset", ""),
                record.get("outer", ""),
            ])
            if expected_id in combined:
                matched = record
                break

        if matched is None:
            failures.append(f"{slug}: no se encontró el ID original {expected_id}")
            continue

        source = matched.get("src") or matched.get("rawSrc") or matched.get("dataSrc") or ""
        id_match = re.search(r"sitesv-images-rt/([^=?]+)", source)
        actual_id = id_match.group(1) if id_match else expected_id
        data, content_type = download_original(page, matched)
        if not data:
            failures.append(f"{slug}: no se pudo descargar la imagen original")
            continue

        destination = DEST / f"{slug}.webp"
        try:
            dimensions = save_lossless_webp(data, content_type or "image/*", destination)
            matched_ids[slug] = actual_id
            print(
                f"OK {slug}: {dimensions[0]}x{dimensions[1]} "
                f"({destination.stat().st_size} bytes)"
            )
        except Exception as error:
            failures.append(f"{slug}: {error}")

    browser.close()

if failures:
    for failure in failures:
        print("ERROR:", failure)
    raise SystemExit(f"No se completó la copia de los 15 logos ({len(failures)} pendientes).")

new_lines = ["const LOGOS = {"]
for slug in LOGOS:
    new_lines.append(f'  "{slug}": "{matched_ids[slug]}",')
new_lines.append("};")
WORKER = re.sub(r"const LOGOS\s*=\s*\{.*?\};", "\n".join(new_lines), WORKER, count=1, flags=re.S)
WORKER_PATH.write_text(WORKER, encoding="utf-8")

print(f"LISTO: 15 logotipos originales guardados en {DEST}; IDs del Worker verificados.")
