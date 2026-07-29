(() => {
  const COURSE = "Deep Learning with PyTorch";
  const INDEX = "/index.html";

  function isPrintPdf() {
    return (
      /print-pdf/i.test(window.location.search) ||
      /view=print/i.test(window.location.search) ||
      document.documentElement.classList.contains("print-pdf") ||
      document.documentElement.classList.contains("reveal-print") ||
      document.body.classList.contains("print-pdf")
    );
  }

  function parsePath() {
    const path = location.pathname || "";
    const moduleMatch = path.match(/\/modules\/M(\d+)\//i);
    const chapterMatch = path.match(/\/ch(\d+)_[^/]+\//i);
    const fileMatch = path.match(/\/([^/]+)\.html?$/i);
    const fileBase = fileMatch ? fileMatch[1] : "";
    const numMatch = fileBase.match(/^(\d+)_/);

    return {
      moduleNum: moduleMatch ? moduleMatch[1] : null,
      chapterNum: chapterMatch ? chapterMatch[1] : null,
      fileNum: numMatch ? numMatch[1] : null,
    };
  }

  function deckTitle() {
    const titleEl =
      document.querySelector(".reveal .quarto-title-block h1.title") ||
      document.querySelector(".reveal .quarto-title-block h1") ||
      document.querySelector(".reveal section.quarto-title-block h1") ||
      document.querySelector('meta[name="dcterms.title"]');
    if (titleEl) {
      return (titleEl.content || titleEl.textContent || "").trim();
    }
    return (document.title || "")
      .replace(/^Deep Learning with PyTorch\s*[—–|-]\s*/i, "")
      .trim();
  }

  function lectureLabel(pathInfo) {
    const title = deckTitle();
    if (pathInfo.fileNum && title) return `${pathInfo.fileNum} ${title}`;
    return title || "Lecture";
  }

  function readAuthor() {
    const selectors = [
      ".reveal .quarto-title-block .quarto-title-author-name",
      ".reveal .quarto-title-author-name",
      ".reveal .quarto-title-block .author",
      'meta[name="author"]',
    ];
    for (const sel of selectors) {
      const node = document.querySelector(sel);
      if (!node) continue;
      const text = (node.content || node.textContent || "").trim();
      if (text) return text;
    }
    return "";
  }

  function readDate() {
    const selectors = [
      ".reveal .quarto-title-block .date",
      ".reveal section.quarto-title-block .date",
      'meta[name="dcterms.date"]',
      'meta[name="date"]',
    ];
    for (const sel of selectors) {
      const node = document.querySelector(sel);
      if (!node) continue;
      const text = (node.content || node.textContent || "").trim();
      if (text) return text;
    }
    return "";
  }

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function link(href, className, text, title) {
    const a = el("a", className, text);
    a.href = href;
    if (title) a.title = title;
    return a;
  }

  function button(className, text, title, onClick) {
    const b = el("button", className, text);
    b.type = "button";
    if (title) b.title = title;
    if (onClick) {
      b.addEventListener("click", (e) => {
        e.preventDefault();
        onClick();
      });
    }
    return b;
  }

  function sep() {
    return el("span", "slide-chrome-sep", ">");
  }

  function h1InfoForSlide(slide) {
    if (!slide || slide.classList.contains("quarto-title-block")) return null;

    let stack = slide;
    if (
      slide.parentElement &&
      slide.parentElement.tagName === "SECTION" &&
      slide.parentElement.parentElement &&
      slide.parentElement.parentElement.classList.contains("slides")
    ) {
      stack = slide.parentElement;
    }

    const level1 =
      stack.querySelector(":scope > section.level1") ||
      (slide.classList.contains("level1") ? slide : null);
    const h1 = level1
      ? level1.querySelector(":scope > h1")
      : stack.querySelector(":scope > h1");
    if (!h1) return null;

    const text = h1.textContent.trim();
    if (!text) return null;

    const slidesRoot = document.querySelector(".reveal .slides");
    if (!slidesRoot) return { text, horizontal: null };

    const horizontalSections = Array.from(slidesRoot.children).filter(
      (n) => n.tagName === "SECTION"
    );
    let horizontal = horizontalSections.indexOf(stack);
    if (horizontal < 0) horizontal = horizontalSections.indexOf(slide);

    return { text, horizontal: horizontal >= 0 ? horizontal : null };
  }

  function currentH1Info(Reveal) {
    return h1InfoForSlide(Reveal.getCurrentSlide());
  }

  function slideProgress(Reveal) {
    const total = Reveal.getTotalSlides();
    const past =
      typeof Reveal.getSlidePastCount === "function"
        ? Reveal.getSlidePastCount()
        : 0;
    const current = Math.min(past + 1, total || 1);
    return { current, total: total || 1 };
  }

  function annotateSlides(Reveal) {
    const slides =
      typeof Reveal.getSlides === "function" ? Reveal.getSlides() : [];
    const total = slides.length || Reveal.getTotalSlides() || 1;
    slides.forEach((slide, idx) => {
      slide.dataset.chromeIndex = String(idx + 1);
      slide.dataset.chromeTotal = String(total);
      const h1 = h1InfoForSlide(slide);
      if (h1 && h1.text) slide.dataset.chromeH1 = h1.text;
      else delete slide.dataset.chromeH1;
    });
  }

  function buildChrome({ forPrint } = {}) {
    const pathInfo = parsePath();
    const top = el(
      "nav",
      forPrint ? "slide-chrome-top" : "slide-chrome-top slide-chrome-global"
    );
    top.setAttribute("aria-label", "Slide breadcrumb");

    const crumbs = el("div", "slide-chrome-crumbs");

    crumbs.appendChild(
      link(INDEX, "slide-chrome-home", "⌂", "Back to course index")
    );

    if (pathInfo.moduleNum) {
      crumbs.appendChild(sep());
      crumbs.appendChild(
        link(
          `${INDEX}#module-${pathInfo.moduleNum}`,
          "slide-chrome-link",
          `M${pathInfo.moduleNum}`,
          `Module ${pathInfo.moduleNum} on course index`
        )
      );
    }

    if (pathInfo.chapterNum) {
      crumbs.appendChild(sep());
      crumbs.appendChild(
        el("span", "slide-chrome-label", `C${pathInfo.chapterNum}`)
      );
    }

    crumbs.appendChild(sep());
    const lectureBtn = button(
      "slide-chrome-link",
      lectureLabel(pathInfo),
      forPrint ? undefined : "Jump to title slide",
      forPrint
        ? null
        : () => {
            if (window.Reveal) window.Reveal.slide(0);
          }
    );
    lectureBtn.dataset.role = "lecture";
    crumbs.appendChild(lectureBtn);

    const h1Wrap = el("span", "slide-chrome-h1-wrap");
    h1Wrap.hidden = true;
    h1Wrap.appendChild(sep());
    const h1Btn = button(
      "slide-chrome-link",
      "",
      forPrint ? undefined : "Jump to section start",
      null
    );
    h1Btn.dataset.role = "h1";
    h1Wrap.appendChild(h1Btn);
    crumbs.appendChild(h1Wrap);

    top.appendChild(crumbs);

    const bottom = el(
      "footer",
      forPrint
        ? "slide-chrome-bottom"
        : "slide-chrome-bottom slide-chrome-global"
    );
    bottom.setAttribute("aria-label", "Slide metadata");

    const author = el(
      "span",
      "slide-chrome-meta slide-chrome-author",
      readAuthor()
    );
    const course = el("span", "slide-chrome-meta slide-chrome-course", COURSE);
    const date = el("span", "slide-chrome-meta slide-chrome-date", readDate());
    const slides = el("span", "slide-chrome-meta slide-chrome-slides", "");

    bottom.appendChild(author);
    bottom.appendChild(course);
    bottom.appendChild(date);
    bottom.appendChild(slides);

    return { top, bottom, h1Wrap, h1Btn, lectureBtn, author, date, slides };
  }

  function applyDynamic(chrome, { h1Text, current, total, Reveal }) {
    if (!chrome.author.textContent) chrome.author.textContent = readAuthor();
    if (!chrome.date.textContent) chrome.date.textContent = readDate();

    if (h1Text) {
      chrome.h1Wrap.hidden = false;
      chrome.h1Btn.textContent = h1Text;
      if (Reveal) {
        const info = { text: h1Text };
        // Resolve horizontal index from live slide if possible.
        const live = currentH1Info(Reveal);
        chrome.h1Btn.onclick = (e) => {
          e.preventDefault();
          if (live && live.horizontal != null) Reveal.slide(live.horizontal, 0);
        };
      }
    } else {
      chrome.h1Wrap.hidden = true;
      chrome.h1Btn.textContent = "";
    }

    if (current != null && total != null) {
      chrome.slides.textContent = `${current} / ${total}`;
    }
  }

  function updateLive(chrome, Reveal) {
    if (!chrome || !Reveal) return;
    annotateSlides(Reveal);
    const h1 = currentH1Info(Reveal);
    const { current, total } = slideProgress(Reveal);
    applyDynamic(chrome, {
      h1Text: h1 && h1.text,
      current,
      total,
      Reveal,
    });
  }

  function slideFromPdfPage(page) {
    return (
      page.querySelector(":scope > section:not(.stack)") ||
      page.querySelector(":scope > section") ||
      page.querySelector("section")
    );
  }

  function injectPrintChrome(Reveal) {
    annotateSlides(Reveal);
    const pages = document.querySelectorAll(".reveal .slides .pdf-page");
    if (!pages.length) return false;

    let lastH1 = null;
    const totalPages = pages.length;

    pages.forEach((page, pageIdx) => {
      if (page.querySelector(":scope > .slide-chrome-top")) return;

      const slide = slideFromPdfPage(page);
      if (slide && slide.classList.contains("level1")) {
        const h1 = slide.querySelector(":scope > h1");
        const text = h1 && h1.textContent.trim();
        if (text) lastH1 = text;
      }

      const isTitle = slide && slide.classList.contains("quarto-title-block");
      const h1Text = isTitle
        ? null
        : (slide && slide.dataset.chromeH1) || lastH1;

      const current =
        (slide && slide.dataset.chromeIndex) || String(pageIdx + 1);
      const total =
        (slide && slide.dataset.chromeTotal) || String(totalPages);

      const chrome = buildChrome({ forPrint: true });
      applyDynamic(chrome, { h1Text, current, total });
      page.appendChild(chrome.top);
      page.appendChild(chrome.bottom);
    });
    return true;
  }

  function startLive() {
    if (document.querySelector(".slide-chrome-global")) return;

    const chrome = buildChrome({ forPrint: false });
    document.body.appendChild(chrome.top);
    document.body.appendChild(chrome.bottom);

    const bind = (Reveal) => {
      updateLive(chrome, Reveal);
      Reveal.on("slidechanged", () => updateLive(chrome, Reveal));
      Reveal.on("ready", () => updateLive(chrome, Reveal));
    };

    if (window.Reveal && typeof window.Reveal.on === "function") {
      if (window.Reveal.isReady && window.Reveal.isReady()) {
        bind(window.Reveal);
      } else {
        window.Reveal.on("ready", () => bind(window.Reveal));
        setTimeout(() => {
          if (window.Reveal.isReady && window.Reveal.isReady()) {
            bind(window.Reveal);
          }
        }, 0);
      }
    }
  }

  function startPrint() {
    const tryInject = (Reveal) => {
      if (injectPrintChrome(Reveal)) return true;
      return false;
    };

    const run = (Reveal) => {
      annotateSlides(Reveal);
      // PDF pages are created during setup; retry briefly until present.
      let attempts = 0;
      const tick = () => {
        if (tryInject(Reveal) || attempts++ > 40) return;
        setTimeout(tick, 50);
      };
      tick();
    };

    if (window.Reveal && typeof window.Reveal.on === "function") {
      if (window.Reveal.isReady && window.Reveal.isReady()) {
        run(window.Reveal);
      } else {
        window.Reveal.on("ready", () => run(window.Reveal));
        setTimeout(() => {
          if (window.Reveal.isReady && window.Reveal.isReady()) {
            run(window.Reveal);
          }
        }, 0);
      }
    }
  }

  function start() {
    if (isPrintPdf()) startPrint();
    else startLive();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
