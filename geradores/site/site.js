// ===================== CONFIGURAÇÃO — edite aqui =====================
const CFG = {
  whatsapp: "5524000000000",                 // só números, com DDI e DDD  [PREENCHER]
  whatsapp_fmt: "(24) 00000-0000",           // como aparece no site        [PREENCHER]
  telefone: "(24) 0000-0000",                // [PREENCHER]
  email: "contato@centromedicoavelar.com.br",// [PREENCHER]
  email_rh: "rh@centromedicoavelar.com.br",  // [PREENCHER]
  horario: "Segunda a sexta, 8h às 18h",     // [CONFIRMAR]
  rt: "Responsável técnico: nome — CRM 00000",  // [PREENCHER]
  dpo: "Encarregado pelo tratamento de dados: nome e e-mail a definir.", // [PREENCHER]
  cnpj: "00.000.000/0001-00",                // [PREENCHER]
  endereco: "Rua Antônio de Mattos, 260 - Avelar, Paty do Alferes - RJ, 26950-000",
  lat: "",  // opcional: coordenadas exatas da entrada (Google Maps → botão direito → copiar)
  lng: "",
  instagram: "https://instagram.com/",       // [PREENCHER]
  facebook: "https://facebook.com/",         // [PREENCHER]
  frames: "assets/frames/f{n}.jpg",          // sequência de quadros do vídeo da marca (hero)
  n_frames: __NFRAMES__,
};
// =====================================================================
const PAGES = __PAGES__;
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const app = $('#app'), hdr = $('#hdr');
function wa(msg){ return 'https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(msg); }
function geo(){ return (CFG.lat && CFG.lng) ? (CFG.lat + ',' + CFG.lng) : CFG.endereco; }
const GEO = {
  maps:  () => 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(geo()),
  rota:  () => 'https://www.google.com/maps/dir/?api=1&destination=' + encodeURIComponent(geo()) + '&travelmode=driving',
  waze:  () => (CFG.lat && CFG.lng) ? ('https://waze.com/ul?ll=' + CFG.lat + ',' + CFG.lng + '&navigate=yes') : ('https://waze.com/ul?q=' + encodeURIComponent(CFG.endereco) + '&navigate=yes'),
  apple: () => 'https://maps.apple.com/?daddr=' + encodeURIComponent(geo()),
  embed: () => 'https://www.google.com/maps?q=' + encodeURIComponent(geo()) + '&z=17&hl=pt-BR&output=embed',
};
const TITLES = {inicio:'Centro Médico Avelar',clube:'Clube CMA+ Benefícios',especialidades:'Especialidades',exames:'Exames',enfermagem:'Enfermagem',unidade:'Unidade',contato:'Contato',indica:'Amigo Indica',trabalhe:'Trabalhe Conosco',cliente:'Área do Cliente',privacidade:'Política de Privacidade',regulamento:'Regulamentos'};

// ---------- toast ----------
let toastT;
function toast(t){ const el = $('#toast'); $('#toast-t').textContent = t; el.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => el.classList.remove('show'), 2600); }

// ---------- menu mobile ----------
const mm = $('#mobile-menu');
function menu(open){ mm.classList.toggle('open', open); mm.setAttribute('aria-hidden', String(!open)); $('#open-menu').setAttribute('aria-expanded', String(open)); document.body.style.overflow = open ? 'hidden' : ''; }
$('#open-menu').addEventListener('click', () => menu(true));
$('#close-menu').addEventListener('click', () => menu(false));
$$('#mobile-menu a').forEach(a => a.addEventListener('click', () => menu(false)));
document.addEventListener('keydown', e => { if (e.key === 'Escape') menu(false); });

// ---------- vínculos (WhatsApp, config, formulários) ----------
function bind(root){
  $$('[data-wa]', root).forEach(a => { a.href = wa(a.dataset.wa); a.target = '_blank'; a.rel = 'noopener'; });
  $$('[data-cfg-text]', root).forEach(el => { el.textContent = CFG[el.dataset.cfgText] || ''; });
  $$('[data-cfg]', root).forEach(a => {
    const k = a.dataset.cfg;
    if (k === 'tel') a.href = 'tel:' + CFG.telefone.replace(/\D/g, '');
    else if (k === 'mail') a.href = 'mailto:' + CFG.email;
    else if (GEO[k]) { a.href = GEO[k](); a.target = '_blank'; a.rel = 'noopener'; }
    else if (k === 'interativo') { a.href = '#'; a.addEventListener('click', e => { e.preventDefault(); const f = $('iframe[data-embed]'); if (f) { f.src = GEO.embed(); f.hidden = false; a.hidden = true; } else window.open(GEO.maps(), '_blank', 'noopener'); }); }
    else if (k === 'copiar') { a.href = '#'; a.addEventListener('click', e => { e.preventDefault(); if (navigator.clipboard) navigator.clipboard.writeText(CFG.endereco).then(() => toast('Endereço copiado')); }); }
    else { a.href = CFG[k] || '#'; if (/^https?:/.test(CFG[k] || '')) { a.target = '_blank'; a.rel = 'noopener'; } }
  });
  $$('[data-social]', root).forEach(a => { a.href = CFG[a.dataset.social]; a.target = '_blank'; a.rel = 'noopener'; });
  $$('form[data-form]', root).forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const kind = f.dataset.form;
    if (kind === 'cliente') { toast('Área do Cliente em implantação — solicite seu acesso pelo WhatsApp.'); return; }
    const fd = new FormData(f), linhas = [];
    for (const [k, v] of fd.entries()) if (v && v !== 'on') linhas.push(k + ': ' + v);
    const head = {clube:'Solicitação de adesão ao Clube CMA+', contato:'Mensagem pelo site', indica:'Indicação — Amigo Indica', trabalhe:'Cadastro no banco de talentos'}[kind];
    const corpo = head + '\n' + linhas.join('\n');
    if (kind === 'trabalhe') location.href = 'mailto:' + CFG.email_rh + '?subject=' + encodeURIComponent(head) + '&body=' + encodeURIComponent(corpo + '\n\n(Anexe seu currículo em PDF a este e-mail.)');
    else window.open(wa(corpo), '_blank', 'noopener');
    toast('Abrindo o canal de envio…');
  }));
  // glow que segue o mouse (bento)
  $$('[data-bento-grid]', root).forEach(g => g.addEventListener('mousemove', e => {
    $$('.bento-card', g).forEach(c => { const r = c.getBoundingClientRect(); c.style.setProperty('--mouse-x', (e.clientX - r.left) + 'px'); c.style.setProperty('--mouse-y', (e.clientY - r.top) + 'px'); });
  }));
  // vídeo: pausar / retomar
  $$('[data-video-toggle]', root).forEach(b => b.addEventListener('click', () => {
    const v = b.closest('.vcard').querySelector('video'); if (v.paused) { v.play(); b.classList.remove('paused'); } else { v.pause(); b.classList.add('paused'); }
  }));
  // ripple
  $$('.btn', root).forEach(b => b.addEventListener('click', e => {
    const r = b.getBoundingClientRect(), s = document.createElement('span'); s.className = 'ripple';
    const d = Math.max(r.width, r.height); s.style.cssText = `width:${d}px;height:${d}px;left:${e.clientX - r.left - d/2}px;top:${e.clientY - r.top - d/2}px`;
    b.appendChild(s); setTimeout(() => s.remove(), 650);
  }));
}

// ---------- revelação ao rolar ----------
let io;
function observe(root){
  if (io) io.disconnect();
  io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); } }), {threshold: .1});
  $$('.scroll-reveal', root).forEach(el => io.observe(el));
  $$('.scroll-reveal', document.querySelector('footer')).forEach(el => io.observe(el));
}

// ---------- hero: a marca surge com o scroll (sequência de quadros em canvas) ----------
const hero = { el: null, cv: null, ctx: null, imgs: [], last: -1, active: false };
function heroSetup(){
  hero.el = $('#hero'); hero.cv = $('#scrub'); hero.active = !!hero.el;
  if (!hero.active) return;
  hero.ctx = hero.cv.getContext('2d'); hero.last = -1;
  if (!hero.imgs.length) {
    for (let i = 1; i <= CFG.n_frames; i++) {
      const im = new Image(); im.decoding = 'async';
      im.src = CFG.frames.replace('{n}', String(i).padStart(3, '0'));
      im.onload = () => { hero.loaded = (hero.loaded || 0) + 1; if (i === 1 || i === hero.lastWanted || hero.loaded === CFG.n_frames) heroUpdate(true); };
      hero.imgs.push(im);
    }
  }
  heroResize(); heroUpdate(true);
}
function heroResize(){
  if (!hero.active) return;
  const r = hero.cv.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
  hero.cv.width = Math.round(r.width * dpr); hero.cv.height = Math.round(r.height * dpr); hero.last = -1;
}
function heroDraw(i){
  const im = hero.imgs[i]; hero.lastWanted = i + 1;
  if (!im || !im.complete || !im.naturalWidth) { // usa o último quadro carregado antes deste
    for (let j = i; j >= 0; j--) if (hero.imgs[j].complete && hero.imgs[j].naturalWidth) { i = j; break; }
    if (!hero.imgs[i].complete) return;
  }
  const cw = hero.cv.width, ch = hero.cv.height, img = hero.imgs[i];
  const s = Math.max(cw / img.naturalWidth, ch / img.naturalHeight), w = img.naturalWidth * s, h = img.naturalHeight * s;
  hero.ctx.clearRect(0, 0, cw, ch); hero.ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
}
function heroUpdate(force){
  if (!hero.active || !hero.el.isConnected) return;
  const vh = window.innerHeight, rect = hero.el.getBoundingClientRect();
  const total = Math.max(1, hero.el.offsetHeight - vh);
  let p = reduce ? 1 : Math.min(1, Math.max(0, -rect.top / total));
  const fi = Math.round(Math.min(1, p / .5) * (CFG.n_frames - 1));
  if (fi !== hero.last || force) { heroDraw(fi); hero.last = fi; }
  const pb = $('#pbar'); if (pb) pb.style.width = (Math.min(1, p / .5) * 100) + '%';
  hero.el.classList.toggle('s2', p > .06); hero.el.classList.toggle('s3', p > .16); hero.el.classList.toggle('s4', p > .3);
  hdr.classList.toggle('logo-on', p > .55);           // a logo aparece no cabeçalho quando a marca já surgiu
  hdr.classList.toggle('scrolled', rect.bottom - vh < 40 || p > .55);
}
let ticking = false;
window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { heroUpdate(); ticking = false; }); } }, {passive: true});
window.addEventListener('resize', () => { heroResize(); heroUpdate(true); });

// ---------- roteador ----------
function render(){
  const key = (location.hash.replace('#/', '') || 'inicio').split('?')[0];
  const page = PAGES[key] ? key : 'inicio';
  app.innerHTML = PAGES[page];
  document.body.classList.toggle('home', page === 'inicio');
  $$('[data-nav]').forEach(a => a.classList.toggle('on', a.dataset.nav === page));
  hdr.classList.remove('logo-on', 'scrolled');
  menu(false);
  window.scrollTo({top: 0, behavior: 'instant'});
  bind(app);
  document.title = (TITLES[page] || 'Centro Médico Avelar') + (page === 'inicio' ? '' : ' — Centro Médico Avelar');
  observe(app);
  $$('.reveal-active', app).forEach(el => { el.classList.remove('reveal-active'); requestAnimationFrame(() => el.classList.add('reveal-active')); });
  hero.active = false;
  if (page === 'inicio') heroSetup();
}
window.addEventListener('hashchange', render);
bind(document.body); render();
$('#ano').textContent = new Date().getFullYear();
