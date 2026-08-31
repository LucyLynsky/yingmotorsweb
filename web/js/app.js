window.YM = window.YM || {};

// Get a key at https://web3forms.com using inbox yingmotorsinfo@gmail.com, then paste it here.
YM.WEB3FORMS_ACCESS_KEY = "d8362f0a-dfa3-4d03-821e-58d364ca7f3e";
YM.WEB3FORMS_ENDPOINT = "https://api.web3forms.com/submit";

YM.t = function (key) {
  var lang = YM.getLang();
  var pack = YM_I18N[lang] || YM_I18N.en;
  return pack[key] || YM_I18N.en[key] || key;
};

YM.applyI18n = function () {
  var lang = YM.getLang();
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach(function (node) {
    node.textContent = YM.t(node.getAttribute("data-i18n"));
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(function (node) {
    node.setAttribute("placeholder", YM.t(node.getAttribute("data-i18n-placeholder")));
  });
  document.querySelectorAll(".lang-btn").forEach(function (btn) {
    btn.classList.toggle("is-active", btn.dataset.lang === lang);
  });
  var titleKey = document.body.getAttribute("data-title");
  if (titleKey) {
    document.title = YM.t(titleKey) + " · YING MOTORS";
  }
};

YM.page = function () {
  return document.body.getAttribute("data-page") || "home";
};

YM.icoSvg = function (name, className) {
  var paths = {
    person: '<circle cx="12" cy="8" r="3.2"/><path d="M5.5 20c.8-3.4 3.4-5.2 6.5-5.2S17.7 16.6 18.5 20"/>',
    whatsapp: '<path d="M5 19.2l.7-2.6A7.8 7.8 0 1 1 12 19.8a8 8 0 0 1-3.3-.7L5 19.2z"/><path d="M9.2 9.6c.2-.5.3-.5.6-.5h.5c.2 0 .4.1.5.4l.5 1.2c.1.3 0 .5-.2.7l-.4.4a5.5 5.5 0 0 0 2.3 2.3l.4-.3c.2-.2.5-.3.7-.1l1.1.6c.3.2.3.4.3.6 0 .3-.2.7-.5.9-.3.2-.7.4-1.3.4-2.2 0-4.8-1.9-6-4.2-.5-1-.6-1.9-.4-2.5.1-.4.4-.7.7-.8z"/>',
    email: '<path d="M4 7h16v11H4z"/><path d="M4 7l8 6 8-6"/>',
    wechat: '<path d="M8 11.5c.4-3.2 3.2-5.5 6.4-5.2 2.8.2 5 2.4 5.3 5.2.2 2.2-.8 4.2-2.6 5.4l.4 2.6-2.6-1.1c-.8.2-1.6.3-2.4.2-3.4-.2-6.1-2.8-6.5-6.1-.1-.4-.1-.7 0-1z"/><path d="M6.2 17.2c-1.5-1-2.4-2.6-2.5-4.4-.3-3.6 2.3-6.8 5.8-7.4"/>',
    search: '<circle cx="11" cy="11" r="6.2"/><path d="M16.2 16.2L21 21"/>'
  };
  return '<span class="' + (className || "contact-ico") + '" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round">' + (paths[name] || "") + "</svg></span>";
};

YM.escapeHtml = function (s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
};

YM.greetingCopyBlock = function () {
  return (
    '<p class="contact-greeting">' + YM.escapeHtml(YM.contactGreeting()) + "</p>" +
    '<button type="button" class="btn btn-ghost dark btn-sm wx-copy-greeting" data-i18n="contact_copy_greeting">' +
      YM.escapeHtml(YM.t("contact_copy_greeting")) +
    "</button>"
  );
};

YM.copyContactGreeting = function (btn) {
  var text = YM.contactGreeting();
  var done = function () {
    if (!btn) return;
    btn.textContent = YM.t("contact_copied");
    btn.classList.add("is-copied");
    setTimeout(function () {
      btn.textContent = YM.t("contact_copy_greeting");
      btn.classList.remove("is-copied");
    }, 1400);
  };
  var fallback = function () {
    try {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      done();
    } catch (err) {}
  };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(fallback);
  } else {
    fallback();
  }
};

YM.bindGreetingCopy = function () {
  if (YM._greetingCopyBound) return;
  YM._greetingCopyBound = true;
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".wx-copy-greeting");
    if (!btn) return;
    e.preventDefault();
    YM.copyContactGreeting(btn);
  });
};

YM.applyContactLinks = function () {
  var wa = YM.whatsappLink();
  var mail = YM.mailtoLink();
  document.querySelectorAll('a[href*="wa.me/8618053729906"]').forEach(function (a) {
    a.href = wa;
  });
  document.querySelectorAll('a[href^="mailto:yingmotorsinfo@gmail.com"]').forEach(function (a) {
    a.href = mail;
  });
  var greeting = YM.contactGreeting();
  document.querySelectorAll(".contact-greeting").forEach(function (p) {
    p.textContent = greeting;
  });
  document.querySelectorAll(".wx-pop").forEach(function (pop) {
    if (pop.querySelector(".contact-greeting")) return;
    var block = document.createElement("div");
    block.className = "wx-greeting-block";
    block.innerHTML = YM.greetingCopyBlock();
    pop.appendChild(block);
  });
  ["wechat", "whatsapp"].forEach(function (id) {
    var item = document.querySelector(".contact-item#" + id);
    if (!item || item.querySelector(".contact-greeting")) return;
    var qr = item.querySelector(".qr-card, img");
    var scan = item.querySelector(".contact-scan");
    var block = document.createElement("div");
    block.className = "contact-greeting-block";
    block.innerHTML = YM.greetingCopyBlock();
    if (qr && qr.parentNode) {
      qr.parentNode.insertBefore(block, qr.nextSibling);
    } else if (scan && scan.parentNode) {
      scan.parentNode.insertBefore(block, scan.nextSibling);
    }
  });
};

YM.contactLine = function (icon, labelKey, valueHtml, extraHtml) {
  return (
    '<div class="contact-item">' +
      YM.icoSvg(icon) +
      "<div>" +
        '<p class="contact-label" data-i18n="' + labelKey + '"></p>' +
        '<div class="contact-value">' + valueHtml + "</div>" +
        (extraHtml || "") +
      "</div>" +
    "</div>"
  );
};

YM.mountChrome = function () {
  var header = document.getElementById("site-header");
  var footer = document.getElementById("site-footer");
  var page = YM.page();
  if (header) {
    header.innerHTML =
      '<div class="nav-wrap">' +
        '<a class="brand" href="index.html" aria-label="YING MOTORS">' +
          '<img src="assets/logo-mark-dark.svg" alt="YING MOTORS">' +
        "</a>" +
        '<button class="menu-toggle" type="button" aria-label="Menu" id="menu-toggle">' +
          "<span></span><span></span><span></span>" +
        "</button>" +
        '<div class="nav-panel" id="nav-panel">' +
        '<nav class="nav" id="site-nav">' +
          '<a href="index.html" data-page="home" data-i18n="nav_home">Home</a>' +
          '<a href="products.html" data-page="products" data-i18n="nav_products">Stock</a>' +
          '<a href="about.html" data-page="about" data-i18n="nav_about">About</a>' +
          '<a href="contact.html" data-page="contact" data-i18n="nav_contact">Contact</a>' +
        "</nav>" +
        '<div class="nav-end">' +
          '<div class="lang-switch" role="group" aria-label="Language">' +
            '<button class="lang-btn" type="button" data-lang="en">EN</button>' +
            '<button class="lang-btn" type="button" data-lang="zh">中文</button>' +
          "</div>" +
          '<div class="nav-contacts">' +
            '<div class="nav-wx">' +
              '<button class="btn btn-ghost btn-sm" type="button" id="nav-wx-btn" aria-expanded="false" aria-controls="nav-wx-pop">' +
                YM.icoSvg("wechat") +
                '<span data-i18n="contact_wechat">WeChat</span>' +
              "</button>" +
              YM.wxPopHtml("nav-wx-pop") +
            "</div>" +
            '<a class="btn btn-gold btn-sm" href="' + YM.whatsappLink() + '" target="_blank" rel="noopener">' +
              YM.icoSvg("whatsapp") +
              '<span data-i18n="contact_whatsapp">WhatsApp</span>' +
            "</a>" +
          "</div>" +
        "</div></div>" +
      "</div>" +
      '<form class="header-search" id="header-search-form" role="search" action="products.html" method="get">' +
        '<div class="wrap">' +
          '<label class="stock-search">' +
            '<span class="stock-search-lead">' +
              YM.icoSvg("search", "search-ico") +
              '<span class="stock-search-text" data-i18n="search_label">Search</span>' +
            "</span>" +
            '<input id="stock-search" name="q" type="search" autocomplete="off" enterkeyhint="search" data-i18n-placeholder="search_placeholder">' +
          "</label>" +
        "</div>" +
      "</form>";
    YM.bindHeaderSearch();
    header.querySelectorAll(".nav a").forEach(function (a) {
      if (a.dataset.page === page) a.classList.add("is-active");
    });
    header.querySelector("#menu-toggle").addEventListener("click", function () {
      header.classList.toggle("is-open");
    });
    YM.bindWxPop(
      header.querySelector(".nav-wx"),
      header.querySelector("#nav-wx-btn"),
      header.querySelector("#nav-wx-pop")
    );
    header.querySelectorAll(".lang-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        YM.setLang(btn.dataset.lang);
        location.reload();
      });
    });
  }
  var ctaWx = document.querySelector(".band-wx");
  if (ctaWx) {
    YM.bindWxPop(ctaWx, document.getElementById("cta-wx-btn"), document.getElementById("cta-wx-pop"));
  }
  if (footer) {
    footer.innerHTML =
      '<div class="footer-grid">' +
        '<div>' +
          '<img class="footer-logo" src="assets/logo-mark-dark.svg" alt="YING MOTORS">' +
          '<p class="footer-name">Shandong Yingmotors Co.,Ltd</p>' +
          '<p class="muted" data-i18n="footer_add"></p>' +
        "</div>" +
        '<div>' +
          '<h4 data-i18n="nav_products">Stock</h4>' +
          '<a href="products.html?cat=new" data-i18n="filter_new"></a>' +
          '<a href="products.html?cat=used" data-i18n="filter_used"></a>' +
          '<a href="custom.html" data-i18n="filter_custom"></a>' +
        "</div>" +
        '<div class="footer-contact">' +
          '<h4 class="footer-contact-title" data-i18n="nav_contact">Contact</h4>' +
          YM.contactLine("person", "contact_person", "Kate") +
          YM.contactLine(
            "email",
            "contact_email",
            '<a href="' + YM.mailtoLink() + '">yingmotorsinfo@gmail.com</a>'
          ) +
          YM.contactLine(
            "wechat",
            "contact_wechat",
            "k18053729906",
            '<img class="footer-qr" src="contact/WeChatKate.jpg" alt="WeChat QR Kate YingMotors">'
          ) +
          YM.contactLine(
            "whatsapp",
            "contact_whatsapp",
            '<a href="' + YM.whatsappLink() + '" target="_blank" rel="noopener">+86 180 5372 9906</a>',
            '<img class="footer-qr" src="contact/WhatsApp.png" alt="WhatsApp QR Kate YingMotors">'
          ) +
        "</div>" +
      "</div>" +
      '<p class="footer-copy" data-i18n="footer_copy"></p>';
  }
  if (!document.querySelector(".float-contacts")) {
    var box = document.createElement("div");
    box.className = "float-contacts";
    box.innerHTML =
      '<a class="float-btn wa-float" href="' + YM.whatsappLink() + '" target="_blank" rel="noopener" aria-label="WhatsApp">' +
        YM.icoSvg("whatsapp") +
        '<span data-i18n="float_wa">WhatsApp</span>' +
      "</a>" +
      '<button class="float-btn wx-float" type="button" id="wx-float-btn" aria-expanded="false" aria-controls="wx-pop">' +
        YM.icoSvg("wechat") +
        '<span data-i18n="float_wx">WeChat</span>' +
      "</button>" +
      YM.wxPopHtml("wx-pop");
    document.body.appendChild(box);
    YM.bindWxPop(box, box.querySelector("#wx-float-btn"), box.querySelector("#wx-pop"));
    YM.pinFloatContacts();
  }
};

YM.pinFloatContacts = function () {
  var box = document.querySelector(".float-contacts");
  var heading = document.querySelector(".footer-contact-title");
  if (!box || !heading) return;

  var gap = 20;
  function update() {
    var headingTop = heading.getBoundingClientRect().top;
    var boxHeight = box.offsetHeight;
    var desired = window.innerHeight - headingTop + gap;
    var maxBottom = window.innerHeight - boxHeight - gap;
    if (maxBottom < gap) maxBottom = gap;
    var lift = Math.min(Math.max(desired, gap), maxBottom);
    box.style.setProperty("--float-bottom", lift + "px");
  }

  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  window.addEventListener("load", update);
  var footer = document.getElementById("site-footer");
  if (footer && window.ResizeObserver) {
    new ResizeObserver(update).observe(footer);
  }
};

YM.wxPopHtml = function (id) {
  return (
    '<div class="wx-pop" id="' + id + '" hidden>' +
      '<p class="wx-pop-kicker" data-i18n="contact_wechat">WeChat</p>' +
      '<img src="contact/WeChatKate.jpg" alt="WeChat QR Kate YingMotors">' +
      '<p class="wx-pop-id">k18053729906</p>' +
      '<p class="muted" data-i18n="contact_wechat_scan"></p>' +
      '<div class="wx-greeting-block">' + YM.greetingCopyBlock() + "</div>" +
    "</div>"
  );
};

YM.bindWxPop = function (root, btn, pop) {
  if (!root || !btn || !pop) return;
  btn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = pop.hasAttribute("hidden");
    if (open) {
      pop.removeAttribute("hidden");
      YM.copyContactGreeting(pop.querySelector(".wx-copy-greeting"));
    } else {
      pop.setAttribute("hidden", "");
    }
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
  document.addEventListener("click", function (e) {
    if (!root.contains(e.target)) {
      pop.setAttribute("hidden", "");
      btn.setAttribute("aria-expanded", "false");
    }
  });
};

YM.inquiryValues = function (form) {
  var data = new FormData(form);
  function g(key) { return String(data.get(key) || "").trim(); }
  var country = g("country");
  if (country === "other") {
    country = g("country_other");
  } else if (form.country && form.country.selectedOptions && form.country.selectedOptions[0] && country) {
    country = form.country.selectedOptions[0].textContent.trim();
  }
  return {
    name: g("name"),
    company: g("company"),
    country: country,
    email: g("email"),
    whatsapp: g("whatsapp"),
    phone: g("phone"),
    wechat: g("wechat"),
    product: g("product"),
    port: g("port"),
    message: g("message")
  };
};

YM.validateInquiry = function (form) {
  var v = YM.inquiryValues(form);
  var errors = [];
  form.querySelectorAll(".is-invalid").forEach(function (el) {
    el.classList.remove("is-invalid");
  });
  if (!v.country) {
    var isOther = form.country && form.country.value === "other";
    errors.push(YM.t(isOther ? "form_error_country_other" : "form_error_country"));
    if (isOther && form.country_other) form.country_other.classList.add("is-invalid");
    else if (form.country) form.country.classList.add("is-invalid");
  }
  var hasContact = v.email || v.whatsapp || v.phone || v.wechat;
  if (!hasContact) {
    errors.push(YM.t("form_error_contact"));
    ["email", "whatsapp", "phone", "wechat"].forEach(function (name) {
      if (form[name]) form[name].classList.add("is-invalid");
    });
  } else if (v.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.email)) {
    errors.push(YM.t("form_error_email"));
    if (form.email) form.email.classList.add("is-invalid");
  }
  var box = document.getElementById("form-errors");
  if (box) {
    box.hidden = errors.length === 0;
    box.innerHTML = errors.map(function (msg) { return "<li>" + YM.escapeHtml(msg) + "</li>"; }).join("");
  }
  if (errors.length) {
    var status = document.getElementById("form-status");
    if (status) {
      status.hidden = true;
      status.textContent = "";
    }
  }
  return errors.length === 0;
};

YM.inquiryMessage = function (v) {
  var product = YM.pageProduct();
  var sku = YM.skuOf(product, v && v.product);
  var greeting = YM.contactGreeting(sku ? { sku: sku } : (product || null));
  var lang = YM.getLang();
  if (lang === "zh") {
    return [
      greeting,
      "姓名：" + (v.name || ""),
      "公司：" + (v.company || ""),
      "国家：" + (v.country || ""),
      "邮箱：" + (v.email || ""),
      "WhatsApp：" + (v.whatsapp || ""),
      "电话：" + (v.phone || ""),
      "微信：" + (v.wechat || ""),
      "意向车型：" + (v.product || "现车"),
      "目的港：" + (v.port || ""),
      v.message || ""
    ].join("\n");
  }
  return [
    greeting,
    "Name: " + (v.name || ""),
    "Company: " + (v.company || ""),
    "Country: " + (v.country || ""),
    "Email: " + (v.email || ""),
    "WhatsApp: " + (v.whatsapp || ""),
    "Phone: " + (v.phone || ""),
    "WeChat: " + (v.wechat || ""),
    "Product: " + (v.product || "stock"),
    "Destination port: " + (v.port || ""),
    v.message || ""
  ].join("\n");
};

YM.bindCountrySelect = function (form) {
  var select = form.querySelector("#country");
  var wrap = document.getElementById("country-other-wrap");
  var other = document.getElementById("country-other");
  if (!select) return;
  var lang = YM.getLang();
  var locale = lang === "zh" ? "zh" : "en";
  var countries = (window.YM_COUNTRIES || []).slice().sort(function (a, b) {
    var an = lang === "zh" ? a.zh : a.en;
    var bn = lang === "zh" ? b.zh : b.en;
    return an.localeCompare(bn, locale);
  });
  select.innerHTML = "";
  var placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = YM.t("form_country_placeholder");
  select.appendChild(placeholder);
  countries.forEach(function (c) {
    var opt = document.createElement("option");
    opt.value = c.en;
    opt.textContent = lang === "zh" ? c.zh : c.en;
    select.appendChild(opt);
  });
  var otherOpt = document.createElement("option");
  otherOpt.value = "other";
  otherOpt.textContent = YM.t("form_country_other");
  select.appendChild(otherOpt);

  function syncOther() {
    var show = select.value === "other";
    if (wrap) wrap.hidden = !show;
    if (other) {
      other.disabled = !show;
      if (!show) other.value = "";
    }
  }
  select.addEventListener("change", function () {
    syncOther();
    select.classList.remove("is-invalid");
    if (other) other.classList.remove("is-invalid");
    if (select.value === "other" && other) other.focus();
  });
  syncOther();
};

YM.fillInquiryProduct = function (form) {
  var params = new URLSearchParams(location.search);
  var product = YM.productById(params.get("id") || "");
  if (product && form.product) {
    form.product.value = YM.productRef(product);
  }
};

YM.setInquiryStatus = function (kind, message) {
  var errors = document.getElementById("form-errors");
  var status = document.getElementById("form-status");
  if (kind === "ok") {
    if (errors) {
      errors.hidden = true;
      errors.innerHTML = "";
    }
    if (status) {
      status.hidden = !message;
      status.textContent = message || "";
      if (message) status.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    return;
  }
  if (status) {
    status.hidden = true;
    status.textContent = "";
  }
  if (errors) {
    errors.hidden = !message;
    errors.innerHTML = message ? "<li>" + YM.escapeHtml(message) + "</li>" : "";
    if (message) errors.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
};

YM.resetInquiryForm = function (form) {
  form.reset();
  var wrap = document.getElementById("country-other-wrap");
  var other = document.getElementById("country-other");
  if (wrap) wrap.hidden = true;
  if (other) {
    other.disabled = true;
    other.value = "";
  }
  form.querySelectorAll(".is-invalid").forEach(function (el) {
    el.classList.remove("is-invalid");
  });
  YM.fillInquiryProduct(form);
};

YM.web3formsKey = function () {
  return String(YM.WEB3FORMS_ACCESS_KEY || "").trim();
};

YM.sendInquiryByEmail = function (form, v) {
  var submitBtn = document.getElementById("form-submit");
  var key = YM.web3formsKey();
  if (!key) {
    YM.setInquiryStatus("error", YM.t("form_error_mail_config"));
    return;
  }
  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = YM.t("form_sending");
  }
  YM.setInquiryStatus("ok", "");
  var payload = {
    access_key: key,
    subject: "Inquiry - " + (v.product || "Yingmotors"),
    from_name: "YING MOTORS website",
    name: v.name || "Website visitor",
    company: v.company,
    country: v.country,
    whatsapp: v.whatsapp,
    phone: v.phone,
    wechat: v.wechat,
    product: v.product,
    port: v.port,
    message: YM.inquiryMessage(v)
  };
  if (v.email) {
    payload.email = v.email;
    payload.replyto = v.email;
  }
  fetch(YM.WEB3FORMS_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    },
    body: JSON.stringify(payload)
  })
    .then(function (res) {
      return res.json().then(function (json) {
        return { ok: res.ok, json: json };
      }, function () {
        return { ok: false, json: null };
      });
    })
    .then(function (result) {
      if (result.json && result.json.success) {
        YM.resetInquiryForm(form);
        YM.setInquiryStatus("ok", YM.t("form_ok_mail"));
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = YM.t("form_finished");
        }
        return;
      }
      YM.setInquiryStatus("error", YM.t("form_error_mail_send"));
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = YM.t("form_submit");
      }
    })
    .catch(function () {
      YM.setInquiryStatus("error", YM.t("form_error_mail_send"));
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = YM.t("form_submit");
      }
    });
};

YM.bindInquiryForm = function () {
  var form = document.getElementById("inquiry-form");
  if (!form) return;
  YM.bindCountrySelect(form);
  YM.fillInquiryProduct(form);
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!YM.validateInquiry(form)) return;
    if (form.botcheck && form.botcheck.checked) return;
    YM.sendInquiryByEmail(form, YM.inquiryValues(form));
  });
};

YM.bindHeaderSearch = function () {
  var form = document.getElementById("header-search-form");
  if (!form) return;
  if (document.getElementById("product-grid")) {
    form.addEventListener("submit", function (e) { e.preventDefault(); });
  }
};

YM.revealProductGrid = function (query) {
  var grid = document.getElementById("product-grid");
  var header = document.getElementById("site-header");
  if (!grid || !String(query || "").trim()) return;
  var headerH = header ? header.offsetHeight : 76;
  if (grid.getBoundingClientRect().top <= window.innerHeight * 0.45) return;
  var y = window.scrollY + grid.getBoundingClientRect().top - headerH - 16;
  window.scrollTo({ top: Math.max(0, y), behavior: "smooth" });
};

YM.mountProductList = function () {
  var grid = document.getElementById("product-grid");
  if (!grid) return;
  var params = new URLSearchParams(location.search);
  var current = params.get("cat") || params.get("type") || "all";
  var query = params.get("q") || "";
  var chips = document.querySelectorAll(".filter-chip");
  var filters = document.getElementById("filters");
  var search = document.getElementById("stock-search");
  if (search) search.value = query;

  function setUrl() {
    var qs = [];
    if (current && current !== "all") qs.push("cat=" + encodeURIComponent(current));
    if (query) qs.push("q=" + encodeURIComponent(query));
    history.replaceState(null, "", "products.html" + (qs.length ? "?" + qs.join("&") : ""));
  }

  function apply() {
    var searching = String(query || "").trim() !== "";
    if (filters) filters.hidden = searching;
    chips.forEach(function (c) {
      if (c.dataset.filter) c.classList.toggle("is-active", c.dataset.filter === current);
    });
    var list = YM_PRODUCTS.filter(function (p) {
      if (searching) return YM.matchesQuery(p, query);
      return YM.matchesFilter(p, current);
    });
    if (!list.length) {
      grid.innerHTML = '<p class="empty" data-i18n="' + (query ? "empty_search" : "empty") + '"></p>';
      YM.applyI18n();
      YM.revealProductGrid(query);
      return;
    }
    YM.renderCards(grid, list);
    YM.revealProductGrid(query);
  }

  chips.forEach(function (chip) {
    if (!chip.dataset.filter) return;
    chip.addEventListener("click", function () {
      current = chip.dataset.filter;
      setUrl();
      apply();
    });
  });
  if (search) {
    search.addEventListener("input", function () {
      query = search.value;
      setUrl();
      apply();
    });
  }
  apply();
};

YM.mountProductDetail = function () {
  var root = document.getElementById("product-detail");
  if (!root) return;
  var id = new URLSearchParams(location.search).get("id");
  var product = YM.productById(id);
  if (!product) {
    root.innerHTML = '<p class="empty" data-i18n="empty"></p>';
    return;
  }
  var t = YM.tProduct(product);
  var lang = YM.getLang();
  var badge = product.category === "used" ? (lang === "zh" ? "二手" : "Used") : (lang === "zh" ? "新车" : "New");
  var skuLabel = lang === "zh" ? "现车编号" : "Stock No.";
  var specRows = product.sku ? [[skuLabel, product.sku]].concat(t.specs) : t.specs;
  var main = product.images[0];
  document.title = (product.sku ? product.sku + " · " : "") + t.name + " · YING MOTORS";
  root.innerHTML =
    '<a class="back-link" href="products.html" data-i18n="detail_back"></a>' +
    '<div class="detail-grid">' +
      '<div class="detail-gallery">' +
        '<img id="main-photo" src="' + main + '" alt="' + t.name + '">' +
        (product.images.length > 1
          ? '<div class="thumbs">' + product.images.map(function (src, i) {
              return '<button type="button" class="thumb' + (i === 0 ? " is-active" : "") + '" data-src="' + src + '"><img src="' + src + '" alt=""></button>';
            }).join("") + "</div>"
          : "") +
      "</div>" +
      '<div class="detail-info">' +
        '<span class="badge">' + badge + "</span>" +
        (product.sku
          ? '<p class="detail-sku"><span data-i18n="sku_label"></span> <button type="button" class="sku-copy" data-sku="' + product.sku + '" title="' + (lang === "zh" ? "复制编号" : "Copy stock number") + '">' + product.sku + "</button></p>"
          : "") +
        '<p class="card-brand">' + product.brand + "</p>" +
        "<h1>" + t.name + "</h1>" +
        '<p class="lead">' + t.subtitle + "</p>" +
        "<p>" + t.summary + "</p>" +
        '<p class="spec-disclaimer" data-i18n="detail_note"></p>' +
        '<ul class="highlights">' + t.highlights.map(function (h) { return "<li>" + h + "</li>"; }).join("") + "</ul>" +
        '<div class="detail-actions">' +
          '<a class="btn btn-gold" href="' + YM.whatsappLink(product) + '" target="_blank" rel="noopener" data-i18n="detail_inquiry"></a>' +
          '<a class="btn btn-ghost" href="' + YM.mailtoLink(product) + '">Email</a>' +
          '<div class="detail-wx">' +
            '<button class="btn btn-ghost" type="button" id="detail-wx-btn" aria-expanded="false" aria-controls="detail-wx-pop">' +
              YM.icoSvg("wechat") +
              '<span data-i18n="contact_wechat">WeChat</span>' +
            "</button>" +
            YM.wxPopHtml("detail-wx-pop") +
          "</div>" +
        "</div>" +
      "</div>" +
    "</div>" +
    '<section class="specs-block">' +
      '<h2 data-i18n="detail_specs"></h2>' +
      '<table class="spec-table">' + specRows.map(function (row) {
        return "<tr><th>" + row[0] + "</th><td>" + row[1] + "</td></tr>";
      }).join("") + "</table>" +
      '<p class="spec-disclaimer" data-i18n="detail_note"></p>' +
    "</section>" +
    (product.videos && product.videos.length
      ? '<section class="specs-block"><h2 data-i18n="detail_videos"></h2>' +
        product.videos.map(function (src) {
          return '<video class="detail-video" controls preload="metadata" src="' + src + '"></video>';
        }).join("") + "</section>"
      : "");

    root.querySelectorAll(".thumb").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelector("#main-photo").src = btn.dataset.src;
        root.querySelectorAll(".thumb").forEach(function (t) { t.classList.remove("is-active"); });
        btn.classList.add("is-active");
      });
    });
    var detailWx = root.querySelector(".detail-wx");
    if (detailWx) {
      YM.bindWxPop(detailWx, detailWx.querySelector("#detail-wx-btn"), detailWx.querySelector("#detail-wx-pop"));
    }
    var skuBtn = root.querySelector(".sku-copy");
    if (skuBtn && product.sku) {
      skuBtn.addEventListener("click", function () {
        var done = function () {
          skuBtn.classList.add("is-copied");
          skuBtn.textContent = lang === "zh" ? "已复制" : "Copied";
          setTimeout(function () {
            skuBtn.classList.remove("is-copied");
            skuBtn.textContent = product.sku;
          }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(product.sku).then(done).catch(function () {});
        }
      });
    }
    YM.applyI18n();
  };

YM.mountHome = function () {
  var featured = document.getElementById("featured-grid");
  if (!featured) return;
  var ids = window.YM_FEATURED_IDS || [];
  var list = ids.map(function (id) { return YM.productById(id); }).filter(Boolean);
  if (!list.length) list = YM_PRODUCTS.slice(0, 6);
  YM.renderCards(featured, list);
};

document.addEventListener("DOMContentLoaded", function () {
  YM.mountChrome();
  YM.applyI18n();
  YM.mountHome();
  YM.mountProductList();
  YM.mountProductDetail();
  YM.bindInquiryForm();
  YM.applyContactLinks();
  YM.bindGreetingCopy();
});
