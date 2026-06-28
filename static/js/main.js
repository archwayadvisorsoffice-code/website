/**
 * Volumus Global — Main JS
 * Handles: sticky nav, mobile menu, scroll reveals, stat counters, back-to-top
 */
(function () {
  'use strict';

  // ── Sticky nav ──────────────────────────────────────────────────────────────
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('nav--scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── Mobile hamburger ────────────────────────────────────────────────────────
  const hamburger   = document.querySelector('.nav__hamburger');
  const mobileMenu  = document.querySelector('.nav__mobile');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileMenu.classList.toggle('nav__mobile--open');
      hamburger.classList.toggle('nav__hamburger--open', isOpen);
      hamburger.setAttribute('aria-expanded', String(isOpen));
    });
    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) {
        mobileMenu.classList.remove('nav__mobile--open');
        hamburger.classList.remove('nav__hamburger--open');
        hamburger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Active nav link ─────────────────────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav__link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
      link.classList.add('nav__link--active');
    }
  });

  // ── Scroll progress bar ─────────────────────────────────────────────────────
  const progress = document.querySelector('.scroll-progress');
  if (progress) {
    window.addEventListener('scroll', function () {
      const total  = document.documentElement.scrollHeight - window.innerHeight;
      const pct    = total > 0 ? (window.scrollY / total) * 100 : 0;
      progress.style.width = pct + '%';
    }, { passive: true });
  }

  // ── Scroll reveal ────────────────────────────────────────────────────────────
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal--visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach(function (el) { observer.observe(el); });
  }

  // ── Stat counters ────────────────────────────────────────────────────────────
  function animateCounter(el) {
    const target   = parseFloat(el.dataset.target) || 0;
    const suffix   = el.dataset.suffix || '';
    const prefix   = el.dataset.prefix || '';
    const decimals = el.dataset.decimals ? parseInt(el.dataset.decimals) : 0;
    const duration = 1800;
    const start    = performance.now();

    function update(now) {
      const elapsed  = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const ease     = 1 - Math.pow(1 - progress, 3); // cubic ease-out
      const current  = target * ease;
      el.textContent = prefix + current.toFixed(decimals) + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
  }

  const counterEls = document.querySelectorAll('[data-counter]');
  if (counterEls.length) {
    const counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          counterObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counterEls.forEach(function (el) { counterObserver.observe(el); });
  }

  // ── Back to top ──────────────────────────────────────────────────────────────
  const btt = document.querySelector('.back-to-top');
  if (btt) {
    window.addEventListener('scroll', function () {
      btt.classList.toggle('back-to-top--visible', window.scrollY > 400);
    }, { passive: true });
    btt.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── RFP / Contact form toggle ────────────────────────────────────────────────
  const rfpToggleBtns = document.querySelectorAll('.rfp-toggle__btn');
  const rfpInput      = document.getElementById('is_rfp');
  const rfpFields     = document.getElementById('rfp-fields');

  if (rfpToggleBtns.length) {
    rfpToggleBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        rfpToggleBtns.forEach(b => b.classList.remove('rfp-toggle__btn--active'));
        btn.classList.add('rfp-toggle__btn--active');
        const isRfp = btn.dataset.type === 'rfp';
        if (rfpInput) rfpInput.value = isRfp ? 'yes' : 'no';
        if (rfpFields) rfpFields.classList.toggle('hidden', !isRfp);
      });
    });
  }

  // ── Smooth anchor scroll ─────────────────────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const id = a.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Auto-dismiss flash alerts ────────────────────────────────────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s';
      setTimeout(function () { alert.remove(); }, 500);
    }, 5000);
  });

})();
