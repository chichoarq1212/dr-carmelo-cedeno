const SOURCE_PAGE = "https://sites.google.com/view/drcarmelocedeno/biograf%C3%ADa?pli=1&authuser=0";
const LOGOS = {
  "fundacion-juventudes": "AMxu72sbSIPfDJNcAgdvCgBTuqFxKrLQlIxR7PiBsxJkYtbrW7tAnHIr3Fx5PFDOVTtsxxNLrrFuHgFTahPvUvLvf2dh0TZ4TtYDWpoVoBJipS-TQhl-i786uiZayuFzCW3iuAC2_ENnhcjFlIrGjodkr4-8qXoD3n8YphWyet4_j39tT4rwCX58lk4_FE1q2aE",
  "fundacion-educando-amor": "AMxu72uPk16mQzgSM-IV3TKxQorEo0vSAFbtYKgBCXhNfNhM_ZKgfeQD8CONVE_0fHd9HMjRXYoMFrVJIeR6BIfN3c4QQe9BVfMDY2Fd2A_XeRN-ZioMWqM9al7oE8zmGiYNDiVsS9XVnjZPAqGjBdToeNcc4KDyEK7G985xi56jbsX4WfzKdDWhxu6H-WcM",
  "caballeros-colon": "AMxu72vvKEq6rvxvH3s8r5Iz-Y1Eku83hzxIOb8VbBo-nquTSVV8BukCgiom7ixmUQ6pNbB_DsIAWAW1u2zRPCTQp_0uTDbTjtLL0IEaT825vPgdVauAYGzgTAUWRnXHI4ezZttE6AcjrP4sSdPg3uEdesISSmbqDWesbFosEt3IFAndoy9G_IwNGalMPQqiajI",
  "rotary-international": "AMxu72uPWXI0YV66YSq5bw2XZY-ZC-TNV5lPqmx8299gDytsq9KWLP3cZlNR-2KxVDasbS9u9SuF1J7CPg5ajumHFl03XP4sFb4H_GBnVRqwn-CwGrR5vXAfrZ59CPx7q69ydJR43PtF7a2AzjyskXFTbbbl-kxllz8pzldaVwY2fswjqorEEXaHLg5ZiNjZTNE",
  "lions-international": "AMxu72sypiXyIPnSG7yy6kY_ZAE-zW_-DDGhj_CL6YZ5lXHj8mAJahHFMM4L2LAAOoLYFGjx4gXf0hYar2GQk8HX00N8yVEKVrq32UY88rTtLiesBdgzV1aCfRrLw_hkX_OMTYaEqzQxsd1ptpvn5qXuyTg6amhU16TsbTMYDAfQ-5ZDyglq62oxR-u0cpBvo70",
  "camara-liderazgo": "AMxu72sowdKj4X5cC2bWeDi55h5hikx1vKiFxIuxWd9zfAYWkDZ7P089Gh_WgR-8Ko6YLz4W7MrYgKV2wzPl6ji3hi0kYpd41PJT2hWj__sLfFjifmVAi0F3_WzyJ-5KRpt_yMQ-lmDxVyywp-lVsLzuXgb7YBBRt5zXZ3gbZo_ffphCG0fvwS82xYbGQecz",
  "redlatampp": "AMxu72uu-9ncUHjtkmCNAp3-thI0czBvVUKVOHppklbfQslc-DrArQ_6jFGYVJr0JtRCHvHI9fTtR-r8q4YS9fhECmNe1Go2hSGZB-E4O86qdRqyMQfbrSAqsEuUluPrFy5pRaSC8jlfhbdAKuGDBYsXSWd1hA1VWmYuAwvXL2zs0g5MMtj7aN2OnD-uK28Q0W-W-MEW7NJsiQgc6uoiPH65UjpSASybZeC92rxxN3AZ6GQ",
  "colegio-investigacion-docencia": "AMxu72uLlDcsIajrAaj26tRy5rKaMe6idRgApfUVj4BpiNUxzoKeXGMOSRZtXA9SbvUYEd7WNvuRcrwdMYrv9tRvsGUIJb8KYfJWs3SVe7M3J4Ix8MFkzree-TB1rM_PdFvotTl2d6AB7JwVAfmxNIXtztk5v4XBccMOlmgymI6iM9RAWi8pmP5bnSu-7a5i0IM",
  "programa-ecologico": "AMxu72u7TFoWQ61mt6qnAeip4w7cOYGRPYt9VB9z0N__pFvf9RB_sK1Dk-vvhLpRNmtAPcAQsABcJtRpYGIvqeFxAhzECsviJLqL2o95qxkE85ZXsQudtqdr6WSIifd3XMq11OgpUNRh_AbPhEmhSW5SEDzRtyoq2yRro0eBg4UtlR9P2pHNarH4begAoNUARQR4ILXz4jL6B9-oRzEotkKjrZ9hj60u0p9faf9SWWy31Fo",
  "sociedad-iberoamericana": "AMxu72udjZMeiEMmP6pZ26Ad47TgDVV_ul9g3Ia6GCnXFxBC0Wj6Q_CCak-c9NZMhXPqQn27YrWwelXxnaSiF7WjvGAyqEvN2dDqONqJWxkxSjRYZcXUPcupz0MY9opl_kxLj1CyawjMO-b3Rc81WjxvySOm-ydFuzDCYh2baKJaw7544GAEQRblNPQQ8Ptp",
  "orden-hospitalaria-victoria": "AMxu72t9e8Deem_gIISG-_GWm1Ig1AUYmIIO7xTggtf6ky1zRAyVWJoV-TnRmNpLTbl4ScnKWl6GHxr0ltmfGNm0vxBoHyJ7SsriBo7R3uqojyCTCj188eNVlJ8qUtF39mSy4B_YnrXrA0TsSybLgp1L6MTHiq98GZdseMw0QRH9wgtpfGYHhdNGupJTAUceSv5to7QI6q9rIiuRI1rysZLYwyUFjTZ2jLBjmbj4Z6qesJA",
  "observatorio-iberoamericano": "AMxu72uz6FUdoL7nbEKCCd66-SvI1BuYbhp1lS_qxS9Td-Zx_d-k8rC3uMa6o8CYClkD2zCFiyO0H7BekXMzD8DVE0ZJCPV8pgTNZthoAALhtFZR0X5eerMyLwTrjt4MLC914A-We-wz68cE1gxPYFWb9dSQhOMuz0SpjoQhg9aLPbBBngfZgbtHqTwlhtgnPwYqK3_qXylqYMMTk36QzafF0owgPnGB-baE5mTj6TyQ",
  "alpha-phi-omega": "AMxu72skdiScWyJYwYpCLQOJoVo8KiWTyAqBG2xDsbDw7HiP4692rjt4cQkTm9rXEchWtKa_USZNgCZaDFaqx8GDoFR2tG6c9sLVdM7tlj3Ps3Hrg0yd2Egv2sIoZkz9XBhKXLaFjocjFQ-_gaUBBzyZjeiPSEC4zPzjV4LAiEFI6gZh_Dq4csgWPSCcGSsXMQDSdctZOKBsclaUnPMW2GzpczP9sE3gqJqNV-9HfXoZj6k",
  "voluntarios-cooperativa-juana-diaz": "AMxu72tMwAeRfBvHzBoUz3Ij64o6NaWl2shylzh5e53u_4JzDnH_6XBlv6qtXhkfb_i9KR0SWApSD2FcvkO6iC1uB5uPLPP1OHYrHV3jW45IwcYLtpwGZe-il5x-hUDmW1xxrSCgZOoDlBRO_mtNsifbHtiY6kquT0cIt18CWGF0MRdJeFMRUH_SyqlYWTGkm9s",
  "comites-internacionales": "AMxu72tovc3uwZz1DVGrfSpZmX7oO-3H74iS-jIYXewY6cTR2Y4F-TalhLU3srBrp113fMAcXOty1h7QTp2wVSXzSeRFIWWngP5o-Gqw6k_j0usNmWpConqKe8YC-C85UI_KRojw3ZRUtEqaVjxghfndovPXpTQg8LStoDVCNyZ-sfY5vvg4yyQbNviW4bah"
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
