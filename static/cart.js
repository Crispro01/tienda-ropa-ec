// Carrito de compras CSP — funciona 100% en el navegador (localStorage),
// no requiere cambios en el backend de Flask.

const CART_KEY = "csp_cart";

const ICONS = {
  Camisetas: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M8 3l4 2 4-2 4 4-3 3v11H7V10L4 7z"/></svg>',
  Pantalones: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 3h12l1 8-2 10h-3l-1-9-1 9H9L7 11z"/></svg>',
  Chompas: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 3L6 5 4 9l3 2v10h10V11l3-2-2-4-3-2-2 2z"/><line x1="12" y1="5" x2="12" y2="20"/></svg>',
  Vestidos: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M10 3h4l1 4-2 2 4 12H7l4-12-2-2z"/></svg>',
};

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
  renderCart();
}

function addToCart(id, name, price, categoria) {
  const cart = getCart();
  const existing = cart.find((item) => item.id === id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ id, name, price, categoria, qty: 1 });
  }
  saveCart(cart);
  openCart();
}

function changeQty(id, delta) {
  let cart = getCart();
  const item = cart.find((i) => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    cart = cart.filter((i) => i.id !== id);
  }
  saveCart(cart);
}

function removeItem(id) {
  const cart = getCart().filter((i) => i.id !== id);
  saveCart(cart);
}

function formatMoney(n) {
  return "$" + n.toFixed(2);
}

function renderCart() {
  const cart = getCart();
  const countEl = document.getElementById("cartCount");
  const itemsEl = document.getElementById("cartItems");
  const totalEl = document.getElementById("cartTotal");
  if (!countEl || !itemsEl || !totalEl) return;

  const totalQty = cart.reduce((sum, i) => sum + i.qty, 0);
  countEl.textContent = totalQty;

  if (cart.length === 0) {
    itemsEl.innerHTML = '<p class="cart-empty">Tu carrito está vacío</p>';
    totalEl.textContent = formatMoney(0);
    return;
  }

  itemsEl.innerHTML = cart
    .map((item) => {
      const icon = ICONS[item.categoria] || ICONS.Camisetas;
      return `
        <div class="cart-item" data-cat="${item.categoria}">
          <div class="cart-item-icon">${icon}</div>
          <div class="cart-item-info">
            <p class="cart-item-name">${item.name}</p>
            <p class="cart-item-price">${formatMoney(item.price)} c/u</p>
          </div>
          <div class="qty-control">
            <button onclick="changeQty(${item.id}, -1)" aria-label="Restar">−</button>
            <span>${item.qty}</span>
            <button onclick="changeQty(${item.id}, 1)" aria-label="Sumar">+</button>
          </div>
          <button class="remove-item" onclick="removeItem(${item.id})">Quitar</button>
        </div>`;
    })
    .join("");

  const total = cart.reduce((sum, i) => sum + i.qty * i.price, 0);
  totalEl.textContent = formatMoney(total);
}

function openCart() {
  document.getElementById("cartPanel").classList.add("open");
  document.getElementById("cartOverlay").classList.add("open");
}

function closeCart() {
  document.getElementById("cartPanel").classList.remove("open");
  document.getElementById("cartOverlay").classList.remove("open");
}

document.addEventListener("DOMContentLoaded", () => {
  renderCart();
  const cartBtn = document.getElementById("cartBtn");
  const closeBtn = document.getElementById("closeCart");
  const overlay = document.getElementById("cartOverlay");
  if (cartBtn) cartBtn.addEventListener("click", openCart);
  if (closeBtn) closeBtn.addEventListener("click", closeCart);
  if (overlay) overlay.addEventListener("click", closeCart);

  document.querySelectorAll(".add-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      addToCart(
        parseInt(btn.dataset.id, 10),
        btn.dataset.name,
        parseFloat(btn.dataset.price),
        btn.dataset.cat
      );
    });
  });

  // Filtro por categoría en la navegación del banner
  document.querySelectorAll(".cat-link").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const cat = link.dataset.cat;
      const isActive = link.classList.contains("active");
      document.querySelectorAll(".cat-link").forEach((l) => l.classList.remove("active"));
      document.querySelectorAll(".card").forEach((card) => {
        card.style.display = "block";
      });
      if (!isActive) {
        link.classList.add("active");
        document.querySelectorAll(".card").forEach((card) => {
          card.style.display = card.dataset.cat === cat ? "block" : "none";
        });
      }
      document.querySelector("main")?.scrollIntoView({ behavior: "smooth" });
    });
  });
});
