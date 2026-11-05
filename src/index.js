const SOURCE_PAGE = "https://sites.google.com/view/drcarmelocedeno/organizaciones-a-que-pertenece";
const LOGOS = {
  "fundacion-juventudes": "AMxu72vbiX7RvtCxB8jeMwHqW_rRhL6g-cRPomNWxKJQdlBdlodXUUWL9TEvM5Vfn_dnEU8jJ5NJM0O_mxCoRubeIGhDY_zwIhZLPrOPeyk1M3uS59pUAW1zXDARc9miRgu7abvAwUrDxAuNTbXO5x3D0mXfayGgM8dJBNcCMnYBlkgx_WmqQg81vWl-W2qnEyQ",
  "fundacion-educando-amor": "AMxu72vKnwGZckAjhO1fglCb08SrT8wqXcvJi8aCm5JAOEWD49bgZzec_NmN8SxJ_9X5T8tASV6z3PJ3jN3_7LJZdJltyP1xdwkRcLpqAqa5_JCOb8Hx9BpXr4ZhurkEpwRSv5Uewc5ujOJmGcRExBZlc6bzKMIBrYf9S7Vh8qRVhJI_hzE8pm3zt3NC4Kn6",
  "caballeros-colon": "AMxu72sDguq-vuWfIXVsgcHNr79nC6jYeuLvv0DYfbE6qjWM4wZPb2RMBSHPBEBB-lZMUP5NoVOyT3-r_szzrI1pS7EqgBvBxFnjHCYyp2qXFtfHcpZfmfMbb88Fidskxfzoe8pkECFXElW7ctAjfS0XWbTqG5WBoTA-ML2_Dk24mc5HiFyGDgTf0zfjlKeSSIs",
  "rotary-international": "AMxu72u2iVsXYMY2rHQnOTkgoFdYki-mNMENh2d513M6YLY7VI11tYc87e3ZmVOzxe3BPoJWzVhxzESqkuNdKX8Wev98ZNzyPRCj5SnvlxSzUDB93B9_Q85yeR2OD-2j3VNypGkN6Md4OaT6zsMtTJwZvlGj7M09FwS06x8NCOCyKesKn7fXjK4RlTZKDRMIbJ4",
  "lions-international": "AMxu72sKqfYnlRfBqbX8nj4F7mMrl_ieKt6RZxNFvcodq3v6prSbt9WRupkrV1k4-za0LXQ8Kdz9Tg_sqP-m9tjk-1tZj510FL8THPtk8WgJlYcRY0-_sVArnv5egLJLqmCawP__2e61U7FQHvox7KERrwfMupYmkqZcSYpuorDf1gMjSgNiogVP78sNK2bZJTI",
  "camara-liderazgo": "AMxu72v9DxDhjiirY9UBP5-gm28Le6dXqpzqxjeX4cCiNzen4UXhb8vSAp-ihDmA2Vvc0mVC2pKJxmaUZRc8NltnrE8v17_JlKQmOXlvE9qX2kWy8YErRPGD0q9W4G1Fy_-_1cz-aNGEB-S4FXCQuNS-aSfxs-unPWr1ldaOSQYGouvbCHAjruF_9CtdB0GM",
  "redlatampp": "AMxu72uNHIi61pb6rq-UOHmXZORg0heZXHbvLZLQoN6SkUmDWUxx9TET1wPoLKUcnVXroyW0kXPLrXUwM4LJ21B32XbuNCDE5Mqj5qCIfukezJfemhKq9t2AO_ivLjpAUzVDEXnuKY_Xs5nCJyeLoClXvtvz6QPavT5OTxBjXd-P3npzYsfJdvjJYXRJ9BqFbjM",
  "colegio-investigacion-docencia": "AMxu72vsUWa_np3kCBb7kSWVLnAcUadfr6kJl-GUpF6WTfRqJmIFuKHAokQ-GgneMFBo0fiB0SPpP3MFrZg7ZDriIT2RdQH5egn6LdaVKx5uNTSa215j1IzrXiTz3mjDjmo9XqEovh3_G3oq4Y5NBjqzEXojqBq_cvyqSVXA1e_pf8OmD31m8GWlsxDt-GGwQmedru-KEOgRnmCJsm5kSV0xZU0AuKXIBTQPjBKPVuAyFP4",
  "programa-ecologico": "AMxu72tv9ytTi9LkfHO79ozYt2p0tMgMej6wFMA_HRzrDbwOXfWgJREeEwAgywax02C8q6kTYVsCwgBZW7OdtvKqb2CY7jXyK5UOMh5m_zcY6EvRXezK3ylyhvYviqqKU4TyOQqR9Ek5LOQDjekpimaloK4s8PAafRSPhVT0-kEDrikrF_lsScyup5s5LqczMcNN5vTxOghsUAkyv-n0ijb9fMJWEmz1Vn0R8zHCrxNxV-Q",
  "sociedad-iberoamericana": "AMxu72skHF-WIXdpvIBkcyzCY6kofieVtay3dJw3JPkfLquNDzIZ1FcOfGmB8l3lenTmd2LNIMr7TrAjOIsH0fabBhmNa3tFspovPQ7k6wc8g0Mm8MQBRlnjxoacgLvKXl2BDzcm3iRJgqoCTWiHSkIkgMorSYj-wIokkv1OKB0D6F017ZFUGbVc8q0jlF9u",
  "orden-hospitalaria-victoria": "AMxu72uOOVplJzXhHwHm96H05lEsH5SEFHqDK5dR7s5yFdOuP8tf4h-J5PRk4ASmB3xwDocrERAWJp4abP58-STFPKw1RGF5gEGcQdyYrxh0LQnz41z5UTj4DL2iPOB2ouX5NCDi5N-7EQAkXDDBFxscRmjc9I0cxI29-OYk_2203qD3qy6RsMyDjsJKRhf4-Ns",
  "observatorio-iberoamericano": "AMxu72vmCbN5RlFSBp3v_-feFTq48IgcVn-fdyrPe2S_MAravLbhu3xSgXVn70ZCB9m4Lrpz6MRErH0P-XnJaAfMCkty4RlVbleqoylddtKtk5bpc3xlaN2I4dnAarfCbzL5Muf3TFuZnvCaM6KbHl1fjTNERO54HpmsGaMi_QTz8Sh8axfMDFZJ63CyFAmxZm4CR8CeLRJ7nSBXirOHVf4mNUHEAM73QnIWyjw7Hleb",
  "alpha-phi-omega": "AMxu72urGuBTnABJJLYSY-ITEwOq3aRlDsFC1I_r9gAnaXfcu8yKTZIQvAHKzLt6x8eS1Uirgs6jqGQ739-JkBvoMTAlbj3pi5xkr6Hi8tP6NaQByiNC1s8zzLSM3DEAH1LhVcGUM9RNmdZx-EziZ9k9FCjeKP4e0u9XZpKUDGxuegTZuzoON_nJyEA8GkMjFkKhRbeOtYYnEA4RarWKySDkpd23SJhHss0NO_mYqAfzkb4",
  "voluntarios-cooperativa-juana-diaz": "AMxu72tpOlI-pgm6xjnE-uTy10uH2i6oZT_GavvUwI0b-8FBsi9yHlQR8pZb_VwZpvc1z93ADvkKJ-vNw2YKdUx33d5blo27oEEq0pwhcwlu4bugy2J49VgT51yxZBef72pMRuzqxFeBGZ6M75eSGfILuWtQE5ObIKKN1deFslg_Jb0b0nMmdvjshxWzr_qs",
  "comites-internacionales": "AMxu72sFtSD9B5ElyH3PbEmAuZkyTi2tuWV1gAavEkVUcqnmGnYGBQR7kSUX0OuZkJQQIQ8Lno1MmQnlpRSUwDXQ7g1x7oomDYN0kvI66DCQS3IH0ueWg6afxr58wu-Qpqol_2wEtDU1n13zalT3F429kGvS3YTSMwtgDrMAHVO9SCuTQsm5hUaekpnh3Fuq8x1pZKxqGsR7npgGHZT57XpL5DZKnt3fhUztynSjFG820XQ",
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
