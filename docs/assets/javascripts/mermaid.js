document$.subscribe(() => {
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: document.body.dataset.mdColorScheme === "slate" ? "dark" : "default",
  });

  mermaid.run({
    nodes: document.querySelectorAll(".mermaid"),
  });
});
