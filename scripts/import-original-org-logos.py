#!/usr/bin/env python3
"""Copy the original organization logo images from the Dr. Carmelo Google Site.

The script downloads the existing image files; it does not redraw or recolor them.
Only transparent outer padding is trimmed. The resulting lossless WebP files are
stored locally in public/assets/org-logos/.
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
WORKER = (ROOT / "src/index.js").read_text(encoding="utf-8")
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
BIOGRAPHY_PAGE = source_match.group(1)
OLD_ORGANIZATIONS_PAGE = "https://sites.google.com/view/drcarmelocedeno/organizaciones-a-que-pertenece"
CANDIDATE_PAGES = [BIOGRAPHY_PAGE, OLD_ORGANIZATIONS_PAGE]
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
    ignored = {
        "logotipo", "logo", "original", "de", "del", "la", "el", "y",
        "por", "para", "con", "internacional", "internacional",
    }
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
        if item.get("href") and (
            "organiz" in (item.get("href", "") + " " + item.get("text", "")).lower()
            or "participación" in (item.get("href", "") + " " + item.get("text", "")).lower()
        )
    ]

def image_bytes(page, record, image_id):
    candidates = []
    for value in (record.get("src"), record.get("rawSrc"), record.get("dataSrc")):
        if value:
            candidates.append(urljoin(page.url, value))
    candidates.extend(
        urljoin(page.url, value)
        for value in srcset_urls(record.get("srcset", ""))
    )
    candidates.extend([
        f"https://sites.google.com/sitesv-images-rt/{image_id}=w1600",
        f"https://lh7-rt.googleusercontent.com/rd-sitesv-images-rt/{image_id}=w1600",
        f"https://lh7-rt.googleusercontent.com/rd-sitesv-images-rt/{image_id}",
        f"https://lh7-us.googleusercontent.com/sitesv-images-rt/{image_id}=w1600",
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
                    "Referer": BIOGRAPHY_PAGE,
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
    pending = list(CANDIDATE_PAGES)

    while pending and len(visited) < 8:
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
            page.wait_for_timeout(3500)
            pending.extend(link for link in collect_org_links(page) if link not in visited)
            for _ in range(10):
                page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 700))")
                page.wait_for_timeout(300)
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(700)
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

    # Remove duplicate image records while preserving source-page order.
    unique = []
    seen_records = set()
    for record in records:
        key = (
            record.get("src") or record.get("rawSrc") or record.get("dataSrc"),
            record.get("alt", ""),
        )
        if key not in seen_records:
            seen_records.add(key)
            unique.append(record)
    records = unique

    print(f"Total de imágenes originales inspeccionadas: {len(records)}")
    used_sources = set()
    failures = []

    for slug, image_id in LOGOS.items():
        target_alt = targets.get(slug, slug.replace("-", " "))
        matched = None

        # Prefer the exact Google Sites image ID found in the original page.
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

        # Otherwise match the original image's alt text to the corresponding card.
        if matched is None:
            target_words = normalize(target_alt)
            ranked = []
            for record in records:
                source_words = normalize(record.get("alt", ""))
                source = record.get("src") or record.get("rawSrc") or record.get("dataSrc")
                if not source_words or not source or source in used_sources:
                    continue
                score = len(target_words & source_words) / max(1, len(target_words))
                ranked.append((score, record))
            if ranked:
                ranked.sort(key=lambda item: item[0], reverse=True)
                if ranked[0][0] >= 0.45:
                    matched = ranked[0][1]

        if matched is None:
            failures.append(f"{slug}: no se encontró imagen | alt esperado={target_alt}")
            continue

        data, content_type = image_bytes(page, matched, image_id)
        if not data:
            failures.append(
                f"{slug}: no se pudo descargar | alt fuente={matched.get('alt', '')} "
                f"| url={matched.get('src') or matched.get('rawSrc')}"
            )
            continue

        destination = DEST / f"{slug}.webp"
        try:
            dimensions = save_lossless_webp(data, content_type or "image/*", destination)
            used_sources.add(
                matched.get("src") or matched.get("rawSrc") or matched.get("dataSrc") or ""
            )
            print(
                f"OK {slug}: {dimensions[0]}x{dimensions[1]} "
                f"({destination.stat().st_size} bytes) | alt={matched.get('alt', '')}"
            )
        except Exception as error:
            failures.append(f"{slug}: {error}")

    if failures:
        print("Imágenes detectadas (para diagnóstico):", file=sys.stderr)
        for record in records:
            print(
                f"ALT={record.get('alt', '')!r} SRC={record.get('src') or record.get('rawSrc')!r}",
                file=sys.stderr,
            )
        browser.close()
        for failure in failures:
            print("ERROR:", failure, file=sys.stderr)
        raise SystemExit(f"No se completó la copia de los 15 logos ({len(failures)} pendientes).")

    browser.close()

print(f"LISTO: se copiaron los 15 logotipos originales a {DEST}.")
