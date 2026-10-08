(() => {
  const giscusOrigin = "https://giscus.app";

  const theme = () =>
    document.body.dataset.mdColorScheme === "slate" ? "dark" : "light";

  const updateTheme = () => {
    const frame = document.querySelector("iframe.giscus-frame");
    frame?.contentWindow?.postMessage(
      { giscus: { setConfig: { theme: theme() } } },
      giscusOrigin
    );
  };

  new MutationObserver(updateTheme).observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"],
  });

  document$.subscribe(() => {
    const thread = document.querySelector(".guide-comments__thread");
    if (!thread || thread.querySelector("script")) return;

    const script = document.createElement("script");
    script.src = `${giscusOrigin}/client.js`;
    script.async = true;
    script.crossOrigin = "anonymous";
    script.setAttribute("data-repo", thread.dataset.repo);
    script.setAttribute("data-repo-id", thread.dataset.repoId);
    script.setAttribute("data-category", thread.dataset.category);
    script.setAttribute("data-category-id", thread.dataset.categoryId);
    script.setAttribute("data-mapping", "pathname");
    script.setAttribute("data-strict", "0");
    script.setAttribute("data-reactions-enabled", "1");
    script.setAttribute("data-emit-metadata", "0");
    script.setAttribute("data-input-position", "bottom");
    script.setAttribute("data-theme", theme());
    script.setAttribute("data-lang", "zh-CN");
    script.setAttribute("data-loading", "lazy");
    thread.appendChild(script);
  });
})();
