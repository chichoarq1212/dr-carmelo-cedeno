const SOURCE_PAGE = "https://sites.google.com/view/drcarmelocedeno/organizaciones-a-que-pertenece";
const LOGOS = {
  "fundacion-juventudes": "AMxu72ucazB8ezXPgcBrXiJimbIcgFzblvoCOG_0BUmXG4bg4xtOYNeQPy0jgmZdO4mmHfqoPb5RQ4g4jSIFxtvKlEJ9wQA8ttxAvgethhlnyNhhgtlQP6-LJa_-57Njl2vpyNAgXFJ4UcULDICqVX27NZ05uFo_sIfMml9dmwnKsHqrO_PBHfmksAandVzqjQ",
  "fundacion-educando-amor": "AMxu72sjHordKAeQQr6snCmaRICmse1eGBTfbKZrnLoXFrw57PRjMTrQiC-GxrfhY_bX9hzE6gNq0ZRsW5WKe-IshPcDslFTJ00FX9kW54zBdo2tpi7-uJWkje8J7yL9Q_DZCNS3BZTOaHS5bquwKKktNNi2z3G3CPZJtTfEqxZimZ80IThkhq2hrjej1lGq",
  "caballeros-colon": "AMxu72s-U7-jqpLKZMWIzKJLS1MNdyt8wKny7mTLfiIC-wRFaSmYMKpYOM0VUHRI08NrXvlhOLtHgqNEUYUJJ5bv2Ec0Zk6zvQ3FYbPGtyLhdG4OjAd5NvJ4Vx4O1BWoLZ190kO6phqF8BaPzPSeQtyiN47FGRuoSA5fM0r4SzrfRE9CuWgKIVSqELX1oNy1qMg",
  "rotary-international": "AMxu72vgbUEphoXIFup3PL3uY8_82L0kkvQBUiT2T-osf82xfE2H7TYbCWPONB39Vq5SsbMDQRxx39Hcz81IgHGLb8765eTV2gBbV4IO1O7jiP4iwXXICA6WYLc68gyknChhYKhf9IhckQoIWY568vV1VdD26Gwq6xqEgYqU4k1da1RBEKr6mE24jFFRuVevLHE",
  "lions-international": "AMxu72vRK6QKaB3WPLoWvBdJNOX5bPblCxkWBHHsk40rXo0XhsIFkf-k1X5w28gOv-SeeSuueh0b-lBpRQaMr_LuTWGkr6e1jBhXj1KxsENbtSPGvc_QTlkCsSPFBQzxE6CUaT_waNNd2IjlxniWpyfzTpheeiJk9t5FGpK-Tx91UW7T-Z1_8rU80gwcXDKtX2U",
  "camara-liderazgo": "AMxu72vioyM0diOa9ClfwSex_I9ztV_Xyotj8X656NOufWWdvkPQdy_XliNAkpgD4CuxaTVLwiWV6DUwhcWP-UXrBNYSlsv77B30kvv4zpb1XSIDKefmI6VA88yyVlT2mA2r5KQS4spS4H2h3MyH49JnHxjykJ_YAp18ichkP9-0vJvx_RIZZxvvA2Bp082O",
  "redlatampp": "AMxu72tyoDoq5abwJrwj_VK80bSBO_gjFvXWDWyBCYiMuiC-pfQhnRGChYfDS_DO_Ka6W-o9cdYsxNjTq6yfHAA6_6WiviaYkojxUOxm_dFATsDKR-e79b1FMUcg8S6aLwwqNrg8jHRVdmE7GmHzUI-XB2qVHdCgi-dLcEAwLhek3d2IRtn9PXrcETwr_aDCYutIx1OW2aibQBSXLMuPI1-g7LpmZ-EZJ4iDQpaXGzQ-IFg",
  "colegio-investigacion-docencia": "AMxu72uAitppybAQezTBnyfqm_3ez0bqcGu24pKuYhX0Rh7O9OwBMhV5aYTGwDjpu3T-6uWOCmsWl9WVMGg1WdeX_cgICgw6UynFXSUVkl1THzM8X3P2-8PogTfPR5WKgMGf5oZFr0sVtRZ-6TJZV6fN1-qn0kq-H4w3A2xUkNmi7YXdgQAp9SS8JTypSsBryO0",
  "programa-ecologico": "AMxu72uyM81JxgE5aAatKSQa_evf-s6P1pAXsYfsFV_taXIMuHfHREMpx40snG5CO-sy3fiZnwZbDwbUp-llgBxsrI7ulCtx3n4HxSybHLuQlkRHHbc5yMHyX9rW4pvOnxEsLNd457Os-t7sclFW021XLkjVGcSN7eiHDFFu1J1X1omZuyLvuy4sFjPidk-EPI9rGDRO6QY8rFsM1KvhXXa4RYEgJHp0YOe9CFJTQTL-MW4",
  "sociedad-iberoamericana": "AMxu72twGN949UI3AKzLS7VQe9HjS6OtExEcBzntvoI4x5NmIPVJuUjaqev-nfD9T1Fltoqtdd61-nVrnS1I8MZz-6rb8ZnDNel2bJdTAO6zKllTNi0PsLYcHKMlQxGBiUKhsGTH0PED1YgU_AcrDr9iYwC5CkukdJzBdRJlfPcKNYJdCWoJQriBi_9CEJjE",
  "orden-hospitalaria-victoria": "AMxu72vzcXK1BAQlG-VMBhThqy6JlfdlA0_UKKj7aw3j5ujCggR6RZH2IIRH6A6SaDMjy2OhpQdSVmIjmZoGSldNTX-g9VOrndqgZuwPYJWFL99X-bcCdU9YaDisnArxmJh47Jj8Je2PyD77DlZNnL66wwCSTJf_Ali_ffTMCO-c61YUGin3nr_O2pnrozY5Ry4IA4tyGolDrneFVwMzPkNEmIdGSBGht7nihpg88ZJH_xE",
  "observatorio-iberoamericano": "AMxu72v7mN79xA5M4Iwt4oTff6Ma8CIH_wOwtTGcnYz_uUYbA56I_4-zvAaGkLf6fCNTUJ_pqrxIHlz-UU9Q40VT1c2p3eDBK4ywVJHytStIcprw8n4wrL2PG4GQUC8okjkbArm2OoImgMhPxPhGoFu3_eTYj7apKZKG2RSOkCZkwRavgBLFyRdROMUsyGV_X5NBUtCFht2svfW4ui-SF8JLDdJwjfmgwwbLkdWDzFc-",
  "alpha-phi-omega": "AMxu72vvAOYjYrdPuZH8RGfd4Oigpz9_lnHGZhGnX-ustAoslRk3bRr087GbMqVZJYUKIhlquTFj8wfN1B3HAbFe0_6s50cfzqvN0LLfjwI4T2qLbKpFEBTW8v30yuvSg5AuJky-AlYRdGlmYieKHqFMfmpTWGvRKVMeGi_SQRqJbNKNSPjyhZh09ajcgshoKvQzk707oFYr_OeMiWIlzjDaKkZ-KWqTm48tx7KIE99wx3w",
  "voluntarios-cooperativa-juana-diaz": "AMxu72sTaxQf4BQcIzqHdtuIazLeDIJSHGSlYyL3C113LbASPbI-S6WhtElvzpMMfw8g247RLZBAS7hqdfLJz5GWKxiTrm9q2cHzfJQFHcrsyj_Xpi6m0rRIB95cFdWkSma0-fUm-b5HLjzs-sDkLdv32csgfswTZd0e266nAzw8uR6TwhuuLZWX1LLv6gLOHP0",
  "comites-internacionales": "AMxu72vqgpQYYYtoaVl7wnOm_xS5GygiOzsSS5AqP8tJdaXOnYAtJ6wzueLhXu3qkp67axSsN8rlSI4_VotNGDFcKUJ2WgLFjlsKOSJfd4ov-H1FvtapSciBYD13q8z_J1CwRb6bUizZzBpYyky1LYHIbFgXXkM1srxMlOUoSXNdKzitcm8jeALeJ22keiU2"
};

function isImageResponse(response) {
  return response && response.ok && (response.headers.get("content-type") || "").toLowerCase().startsWith("image/");
}

async function fetchLogo(id) {
  const options = {
    headers: { "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8" },
    referrer: SOURCE_PAGE,
    referrerPolicy: "unsafe-url",
    redirect: "follow",
    cf: { cacheEverything: true, cacheTtl: 86400 }
  };
  const candidates = [
    `https://sites.google.com/sitesv-images-rt/${id}=w1280`,
    `https://lh7-rt.googleusercontent.com/rd-sitesv-images-rt/${id}`,
    `https://lh7-us.googleusercontent.com/sitesv-images-rt/${id}=w1280`
  ];
  for (const source of candidates) {
    try {
      const response = await fetch(source, options);
      if (isImageResponse(response)) return response;
    } catch (_) {}
  }
  return null;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/assets/org-logos/")) {
      const slug = url.pathname.slice("/assets/org-logos/".length);
      const id = LOGOS[slug];
      if (!id) return new Response("Logo no encontrado", { status: 404 });
      // Prefer a locally stored copy of the original logo. This keeps the
      // gallery independent from Google Sites availability and hotlink rules.
      const localUrl = new URL(`/assets/org-logos/${slug}.webp`, url.origin);
      const localResponse = await env.ASSETS.fetch(new Request(localUrl, { method: "GET" }));
      if (localResponse.ok) {
        const headers = new Headers(localResponse.headers);
        headers.set("Cache-Control", "public, max-age=31536000, immutable");
        headers.set("X-Content-Type-Options", "nosniff");
        return new Response(localResponse.body, { status: 200, headers });
      }
      const cacheKey = new Request(url.origin + url.pathname, { method: "GET" });
      const cache = caches.default;
      const cached = await cache.match(cacheKey);
      if (cached) return cached;
      const upstream = await fetchLogo(id);
      if (!upstream) return new Response("No se pudo recuperar el logotipo original", { status: 502, headers: { "Cache-Control": "no-store" } });
      const headers = new Headers(upstream.headers);
      headers.set("Cache-Control", "public, max-age=86400, s-maxage=604800");
      headers.set("X-Content-Type-Options", "nosniff");
      headers.set("Access-Control-Allow-Origin", "*");
      const response = new Response(upstream.body, { status: 200, headers });
      ctx.waitUntil(cache.put(cacheKey, response.clone()));
      return response;
    }
    return env.ASSETS.fetch(request);
  }
};
