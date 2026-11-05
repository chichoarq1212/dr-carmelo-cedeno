#!/usr/bin/env python3
"""Copy original organization logos from the original Google Sites page.

Images are downloaded from their source URLs and saved locally as lossless WebP.
No logo is redrawn, recolored, or otherwise redesigned.
"""
from __future__ import annotations

import base64
import re
import sys
import unicodedata
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
SLUGS = re.findall(r'"([^"]+)"\s*:', logo_block.group(1))

targets = {}
for tag in re.findall(r"<img\b[^>]*data-org-logo[^>]*>", HTML, re.I | re.S):
    src = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.I)
    alt = re.search(r'\balt=["\']([^"\']+)["\']', tag, re.I)
    if src and alt:
        slug = src.group(1).rstrip("/").split("/")[-1]
        if slug.lower().endswith(".webp"):
            slug = slug[:-5]
        targets[slug] = alt.group(1)

if len(SLUGS) != 15 or len(targets) != 15:
    raise SystemExit(
        f"Se esperaban 15 organizaciones; mapa={len(SLUGS)}, tarjetas={len(targets)}."
    )

def normalize(value: str) -> set[str]:
    folded = unicodedata.normalize("NFKD", value.lower())
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    words = re.findall(r"[a-z0-9]+", folded)
    ignored = {
        "logotipo", "logo", "original", "de", "del", "la", "el", "y",
        "por", "para", "con", "las", "los", "asociacion",
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

def frame_snapshot(frame):
    try:
        return frame.locator("body").evaluate(
            """body => {
                const imageData = [...document.images].map(img => {
                    const r = img.getBoundingClientRect();
                    return {
                        src: img.currentSrc || img.src || '',
                        rawSrc: img.getAttribute('src') || '',
                        srcset: img.getAttribute('srcset') || '',
                        dataSrc: img.getAttribute('data-src') || '',
                        alt: img.getAttribute('alt') || '',
                        width: img.naturalWidth || img.width || 0,
                        height: img.naturalHeight || img.height || 0,
                        x: r.x, y: r.y, w: r.width, h: r.height
                    };
                });
                const textData = [...document.querySelectorAll(
                    'h1,h2,h3,h4,h5,p,div,span,li,a,td,th'
                )].map(el => {
                    const text = (el.innerText || el.textContent || '').trim();
                    if (!text || text.length > 360) return null;
                    const r = el.getBoundingClientRect();
                    return {
                        text, x: r.x, y: r.y, w: r.width, h: r.height,
                        tag: el.tagName.toLowerCase()
                    };
                }).filter(Boolean);
                return { images: imageData, texts: textData };
            }"""
        )
    except Exception:
        return {"images": [], "texts": []}

def image_bytes(page, record):
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
    response = page.goto(ORG_PAGE, wait_until="domcontentloaded", timeout=90000)
    if response is None or not response.ok:
        raise SystemExit(f"No se pudo abrir el directorio original: {response.status if response else 'sin respuesta'}.")
    try:
        page.wait_for_load_state("networkidle", timeout=20000)
    except Exception:
        pass
    page.wait_for_timeout(3000)
    for _ in range(12):
        page.evaluate("window.scrollBy(0, Math.max(window.innerHeight, 700))")
        page.wait_for_timeout(300)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(700)

    snapshots = []
    for frame in page.frames:
        snapshot = frame_snapshot(frame)
        if snapshot["images"]:
            snapshots.append({
                "frame_url": frame.url,
                "images": snapshot["images"],
                "texts": snapshot["texts"],
            })

    print(
        f"Directorio original abierto: {page.url} | título={page.title()!r} "
        f"| marcos con imágenes={len(snapshots)}"
    )

    matches = {}
    used_images = set()

    for slug in SLUGS:
        target = targets[slug]
        target_words = normalize(target)
        ranked = []

        for snapshot in snapshots:
            images = [
                image for image in snapshot["images"]
                if "sites.google.com/sitesv-images-rt/" in (
                    image.get("src", "") or image.get("rawSrc", "")
                )
                and int(image.get("width") or 0) >= 24
                and int(image.get("height") or 0) >= 24
            ]
            for text_item in snapshot["texts"]:
                words = normalize(text_item["text"])
                score = len(target_words & words) / max(1, len(target_words))
                if score < 0.45:
                    continue
                tx = text_item["x"] + text_item["w"] / 2
                ty = text_item["y"] + text_item["h"] / 2
                for image in images:
                    source = image.get("src") or image.get("rawSrc") or ""
                    if source in used_images:
                        continue
                    ix = image["x"] + image["w"] / 2
                    iy = image["y"] + image["h"] / 2
                    distance = ((ix - tx) ** 2 + (iy - ty) ** 2) ** 0.5
                    ranked.append((score, distance, image, text_item["text"], snapshot["frame_url"]))

        ranked.sort(key=lambda item: (-item[0], item[1]))
        matched = None
        if ranked:
            best_score, best_distance, best_image, best_text, best_frame = ranked[0]
            # Prefer a text/image pair in the same card or immediately adjacent block.
            if best_score >= 0.45 and best_distance <= 650:
                matched = best_image
                print(
                    f"ASOCIADO {slug}: score={best_score:.2f}, distancia={best_distance:.0f}px, "
                    f"texto={best_text[:120]!r}"
                )

        if matched is None and slug == "comites-internacionales":
            # The final committee emblem is the last remaining source-page logo.
            # The page header emblem is also unused, but it sits at the top;
            # choose the remaining original logo image lowest on the directory.
            remaining = []
            for snapshot in snapshots:
                for image in snapshot["images"]:
                    source_candidate = image.get("src") or image.get("rawSrc") or ""
                    if (
                        "sites.google.com/sitesv-images-rt/" in source_candidate
                        and source_candidate not in used_images
                        and int(image.get("width") or 0) >= 24
                        and int(image.get("height") or 0) >= 24
                    ):
                        remaining.append(image)
            if remaining:
                matched = max(remaining, key=lambda image: image.get("y", 0))
                print(
                    f"ASOCIADO {slug} por posición final: "
                    f"y={matched.get('y', 0):.0f}px"
                )

        if matched is None:
            print(f"NO ASOCIADO {slug}: {target!r}")
            continue

        source = matched.get("src") or matched.get("rawSrc") or ""
        image_id_match = re.search(r"sitesv-images-rt/([^=?]+)", source)
        image_id = image_id_match.group(1) if image_id_match else ""
        if not image_id:
            print(f"ID NO ENCONTRADO para {slug}: {source}")
            continue

        data, content_type = image_bytes(page, matched)
        if not data:
            print(f"DESCARGA FALLIDA para {slug}: {source}")
            continue

        destination = DEST / f"{slug}.webp"
        try:
            dimensions = save_lossless_webp(data, content_type or "image/*", destination)
            used_images.add(source)
            matches[slug] = image_id
            print(
                f"OK {slug}: {dimensions[0]}x{dimensions[1]} "
                f"({destination.stat().st_size} bytes)"
            )
        except Exception as error:
            print(f"PROCESAMIENTO FALLIDO {slug}: {error}")

    browser.close()

if len(matches) != 15:
    raise SystemExit(
        f"Solo se pudieron asociar y guardar {len(matches)} de 15 logotipos originales."
    )

new_lines = ["const LOGOS = {"]
for slug in SLUGS:
    new_lines.append(f'  "{slug}": "{matches[slug]}",')
new_lines.append("};")
new_block = "\n".join(new_lines)
WORKER = re.sub(r"const LOGOS\s*=\s*\{.*?\};", new_block, WORKER, count=1, flags=re.S)
WORKER_PATH.write_text(WORKER, encoding="utf-8")

print(f"LISTO: 15 logotipos originales guardados en {DEST}; IDs del Worker actualizados.")
