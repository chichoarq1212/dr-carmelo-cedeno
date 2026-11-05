const SOURCE_PAGE = "https://sites.google.com/view/drcarmelocedeno/organizaciones-a-que-pertenece";
const LOGOS = {
  "fundacion-juventudes": "AMxu72u9JJXiA6zdj9P3ke2H2u8wZP9N8XlPTFIJTiMn-Od9Y4uDutpUqO7HrN5yUVdxxVYp-ih9pTj3weKcqz82U8n3Fxh11kKsEJdYhv_mAn5g3EYk33pfjycmcdu4fJcVE3_qAIyb66NGAnGxMexMgL0jFPJnrQ4T7g1gRq1Z5M2FMbmXYWxUt65xt_XSnbs",
  "fundacion-educando-amor": "AMxu72vJTuy00ZTGi1puc3tJEObHggYjMfpp-rq7JrE9F97Qn5FL0Tu9xdFUJDPfyinP0xCIejXr6JPqdpdpvN0ILHrPh2jciuHuJvYycTWmXjyPOxKr9PplAsIsuRcxZgLJ5R4vucogJUmkAC5hVM_gXuUIsMqbjtzfQp58esnXoJ34FVOgF3vbyEhfUeQF",
  "caballeros-colon": "AMxu72veYrLnAZHccIQVrXbPne-TmTQDQ68jupL2LAHsmg5IdR_bmAEkHqStFLgiJFzdWUqP7C8sdD3xzvmQJwAOjFO2FCTF8Mi7gkSev3CM5tlqSVlGwsJQQ3WnV6eBQM-VeBbOl8eYKTEfDN8ppeOB2W69bmo8Uz24sPJhEDteV3p9b1w31IZ7OvN_NwTxcNY",
  "rotary-international": "AMxu72seyx3Vgcc1sE_ApqoL8nmBgHWzIONGz7t8bNnMv9LUx1Pm-ip8LfNdjvx2pB-IL5-1BVLYSgFJup1N5jAU92fT-NF1kcu7r8JCeGdd0ZlCAKRiy8MDI3MSAHmPKzSOAstW75AYzXL4wja24Wla7TH2aYCsKNq11NEjRerl8wtok-GxFcVrwyhMEDwuYlw",
  "lions-international": "AMxu72ustCBwjkbPq2rMGQr9tFsTNi8DeV6pGGDSt7q5UrOOIJVog5Wg0slyrw52kBn2Ys_WK5MjXYG4rGdNEE2LIDEPWnemqSxobySfnPcaZ3mt26c7cOTWoMb-fP5dhgahMgqBTM09swUBhiLAJ_3b9LpHjPC3SY_PnIbZf6AhiSjUI5WzwmjC9NGs4Z8MjsY",
  "camara-liderazgo": "AMxu72s1kQo5F5EKAb6g607xdrrYuanwwpmKfYOWDkYsDBdAADDkwXoD0OqgGdDpBmoXej83cgRgvXXrUnI_de-kd5jy9fmeDodl8rOHR3y_5hPK8Yi9vCaIzefAO8ZApLiCyO2MX8sVBY_hxZDxdFIqBB4URH37ANjvhEy8eY9qUB8vSWMG7EKz7LBtbUkH",
  "redlatampp": "AMxu72vLP_gDAG__dd6gT4gI3SJimISV9kN1jKI6zsCavRQTug27A0C--ocLkKkqKdCIwjAB3lfEHC95SVLFq8mbSjrXWu6KWQT0e0iVpV8KFDyoiskN3d2G93BDJ2Am7-HUeSVpMDfX1flkHnX52GOsVlK8wLc8iSIYFW41HDttO3Mg1IzduXrLG2iu-G8Qe9Q",
  "colegio-investigacion-docencia": "AMxu72sFXcpA3X8hVqxpoibQ9dx3winvM8eEgv1gHYcGs82QpSRdRnImb3Uw3SQbKfIY38JzkN4kTKbCJkf4nSoKStFEQl0v831UFVKCkqYTBjfO9cvATO8pukqSehCRLHP3iIdYIAyJD4NTCrOJCAPpWsCot9qRqgZ0klKpmZvW9zFj3p2kY9tp9GMdRcahJ3H2uZjWBRdUoVz-8R-4pmgJHDfJ09aQkloGsRyAVU2BHhY",
  "programa-ecologico": "AMxu72tMA66GAbCptU6jZT03VortD6ng0gKK7rIwPi0O049waElFAvFBabWHyhINPDbnDwk-f7OKnGwF2hYq8Pi2PUfFRnL8TDQakV9byF2znEAGwEDg4yqV1v4xnmZfyYoQWnf35PAuQKgjUBE0MFPViNCUSEFAbDbQ3Tqp4X_lr4Rfpn6qcqTCT3ltHobOuSHK8mAd7mGIR7nwSz7iDbK3po_hzlaslypixyWNLEzX7Ow",
  "sociedad-iberoamericana": "AMxu72s7MnMOOGoLoeY0AA5BmAsN96z-xpfxmqZBmMfEvewTjYrAg77-2McxBVQZOyUVWhLJvLMIHoGP5tQE0dYczWgkIBWiB8DCXBz-eiQDSSUcbNu9BDUSIy1pD27qTOkdqjTGufvjc9apOF0fmiDK08QbkY4q2UUnaCS1hj98BrSWDVV5OGtXf2iStffy",
  "orden-hospitalaria-victoria": "AMxu72sjSD1ZiHZ-CMzHZAILW5-we3iAhQ3Zvlrw2-KyoxczxumLFg4N7iUAT5cYiUKVADsHzm_LB0gm5Ceu-anshUWZYl7hdgiR_ElKSLQ4z_s7J-yK1erbFIS5KkOyNO6Y3E55L7lxY_d3daIunwixGusOO7eTv-CRPU_TDUOe6TRON23WV8PPIKB-w5DPyQY",
  "observatorio-iberoamericano": "AMxu72sz6hLpe69YxWcVpq3pY8giF2CK2cT-PS2YAaQ6IKyY7LZPV7vHNmZYkEEcAV7ZDC50L2qwL5bGXZepIjaUbEBQVSBZAyAQ5_aVH-HR6Y3ROJ4nOWJ9qHy46RKiPS2jbefJCVIphCvyhZkJECRXMtL1VPZQ2IObxWv7CGsXpbhd2x-m93iL_HvWAMMxZaP-lfGFylQ-TwrbTcFr3oyMSz_PgZDGQ_leVopkszQZ",
  "alpha-phi-omega": "AMxu72uOL-wFLjBT4vzj57gp0asuD4uwGNVmRyMhSvhQMns2C5rYeP_LRBR1HYIUUJ__eoRtLzLXqsthxQe544DFwBIOUctHV3L6a0lOCfkhPnoFF7y7ZVPaaS5-83SghOaFpI_MgQ7yqgFEusTrG7ny0dsw9N08cM6UgkvKhKu4OugvjlNwwar0PLMAMau_WNhjPvb7duOb9S10ZSLePuFYDBU17PpdDy9fveSO22K4hAI",
  "voluntarios-cooperativa-juana-diaz": "AMxu72tbSd8b7jpJvJhFa0pFmZ-3R-JaoF9ql33IG52rRAhtFbnD0EHusNjjyM6Tro2JEZgXMjYUmgWxBSEyuF7BMQh0WRvvkynUofxtlLJDQ198X6BjoQzwiYunrBZw1hSoaZgc9GTeSDEeWc6AB0GrE0FGagDDvt-YvHIUc0kIceXKPmWxfHX8G6-iRN8J",
  "comites-internacionales": "AMxu72trxJP140pc3_QDbITZrxPnve-fXQemWNODni8-XexhixnFrAlBTGEG4FwltJrybTItF7k1OW7LRthLsF0xV0_rg4xIyKYXk9cEEQIOXh9dp_lVqnSlftdXCI-IR103fYx-S7UKvIn1BA1g585dWPSUEj9fh-S6XtXYcIhVlF1Mws7vXmWBBE83zLQ6mqhnx5wueX3XSzZXfJgKW-B_YG864RFAlysLaRqHqowMlWI",
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
      const requestedSlug = url.pathname.slice("/assets/org-logos/".length);
      const slug = requestedSlug.replace(/\.webp$/i, "");
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
