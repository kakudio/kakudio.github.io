(function () {
  const config = window.KAKUDIO_CONFIG;
  if (!config) return;

  const isLive = (key) => {
    const url = config.links[key];
    return typeof url === "string" && url.startsWith("https://");
  };

  const removeWithEmptyParent = (el) => {
    const parent = el.parentElement;
    el.remove();
    if (!parent.children.length && !parent.textContent.trim()) parent.remove();
  };

  document.querySelectorAll("[data-field]").forEach((el) => {
    const value = config.randomizer[el.dataset.field];
    if (value) el.textContent = value;
    else el.hidden = true;
  });

  document.querySelectorAll("[data-link]").forEach((el) => {
    const { link, unless } = el.dataset;
    if (isLive(link) && !(unless && isLive(unless))) {
      el.href = config.links[link];
      el.hidden = false;
    } else {
      removeWithEmptyParent(el);
    }
  });

  document.querySelectorAll("[data-link-text]").forEach((el) => {
    const key = el.dataset.linkText;
    if (!isLive(key)) return;
    const link = document.createElement("a");
    link.href = config.links[key];
    link.textContent = el.textContent;
    el.replaceWith(link);
  });

  const media = document.querySelector(".media");
  const items = config.media || [];
  if (!media) return;
  if (!items.length) {
    media.remove();
    return;
  }
  items.forEach((item) => {
    const figure = document.createElement("figure");
    figure.className = "slot";
    const img = document.createElement("img");
    img.src = item.src;
    img.alt = item.alt || "";
    img.loading = "lazy";
    img.decoding = "async";
    figure.append(img);
    media.append(figure);
  });
  media.hidden = false;
})();
