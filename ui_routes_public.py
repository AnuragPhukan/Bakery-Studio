from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ui_utils import page_template


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index():
    # Render the landing page.
    body = """
    <div class="landing">
      <div id="vanta-bg"></div>
      <div class="landing-shell" id="landingContent">
        <nav class="landing-nav">
          <div class="brand">
            <span class="brand-mark" aria-hidden="true">
              <svg viewBox="0 0 64 64" role="img">
                <path d="M12 34c0-11 9-20 20-20s20 9 20 20v14H12V34z" fill="#ffffff" fill-opacity="0.9"/>
                <path d="M20 30c2-6 7-10 12-10s10 4 12 10" stroke="#4f3df5" stroke-width="4" fill="none" stroke-linecap="round"/>
                <circle cx="26" cy="36" r="2.5" fill="#4f3df5"/>
                <circle cx="38" cy="36" r="2.5" fill="#4f3df5"/>
              </svg>
            </span>
            <span>Bakery Quotations</span>
          </div>
          <div class="nav-links">
            <span>Live pricing</span>
            <span>Quote in minutes</span>
            <span>PDF + Email</span>
          </div>
          <div class="nav-actions">
            <a class="nav-cta" href="#admin-panel">Admin login</a>
          </div>
        </nav>
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow">Bakery quoting, elevated</div>
            <h1>Your bakery knowledge, activated everywhere.</h1>
            <p>
              Turn recipes into instant, consistent quotes with live material pricing,
              polished PDFs, and a conversational quoting flow your team can trust.
            </p>
            <div class="hero-actions">
              <a class="primary" href="/chat">Start a quote</a>
            </div>
          </div>
          <div class="hero-visual">
            <div class="visual-bubble user">What's your best selling cake combo?</div>
            <div class="visual-bubble">
              You got it. Here's the most popular combo for this season.
            </div>
            <div class="visual-product">
              <div class="product-image" aria-hidden="true">
                <svg viewBox="0 0 64 64" role="img">
                  <path d="M14 30c0-10 8-18 18-18s18 8 18 18" fill="#fff4ea"/>
                  <path d="M18 30h28v20H18z" fill="#f3c3a2"/>
                  <path d="M22 30c2-5 6-8 10-8s8 3 10 8" stroke="#4f3df5" stroke-width="3" fill="none"/>
                  <circle cx="26" cy="38" r="2" fill="#4f3df5"/>
                  <circle cx="32" cy="42" r="2" fill="#4f3df5"/>
                  <circle cx="38" cy="38" r="2" fill="#4f3df5"/>
                </svg>
              </div>
              <div>
                <div class="product-title">Signature sponge set</div>
                <div class="product-meta">Vanilla cake · Buttercream · Berries</div>
                <button class="mini-btn">Add to quote</button>
              </div>
            </div>
            <div class="visual-total">Purchases <span>+£128k</span></div>
          </div>
        </section>
      </div>
      <div class="dot-wave"></div>
      <div class="admin-overlay" id="adminOverlay">
        <section class="admin-panel" id="admin-panel">
          <h2>Admin pricing</h2>
          <p>Sign in to update material prices for quotes.</p>
          <div id="admin-login" class="admin-row">
            <input id="adminPassword" type="password" placeholder="Admin password" />
            <button id="adminLoginBtn">Unlock pricing</button>
          </div>
          <div id="admin-editor" style="display: none;">
            <table class="admin-table">
              <thead>
                <tr>
                  <th>Material</th>
                  <th>Unit</th>
                  <th>Currency</th>
                  <th>Unit Cost</th>
                  <th>Save</th>
                </tr>
              </thead>
              <tbody id="adminTableBody"></tbody>
            </table>
            <div class="admin-footer">
              <button id="adminLogoutBtn">Log out</button>
              <div class="admin-status" id="adminStatus"></div>
            </div>
          </div>
          <div class="admin-status" id="adminStatusLoggedOut"></div>
        </section>
      </div>
    </div>
    <script src="three.r134.min.js"></script>
    <script src="vanta.waves.min.js"></script>
    <script>
      VANTA.WAVES({
        el: "#vanta-bg",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0xe0e8ff,
        shininess: 60,
        waveHeight: 18,
        waveSpeed: 0.75,
        zoom: 0.85
      });
      const adminOverlay = document.getElementById("adminOverlay");
      const landingContent = document.getElementById("landingContent");
      const dotWave = document.querySelector(".dot-wave");
      const adminLogin = document.getElementById("admin-login");
      const adminEditor = document.getElementById("admin-editor");
      const adminStatus = document.getElementById("adminStatus");
      const adminStatusLoggedOut = document.getElementById("adminStatusLoggedOut");
      const adminTableBody = document.getElementById("adminTableBody");

      function setStatus(message) {
        adminStatus.textContent = message;
        adminStatusLoggedOut.textContent = message;
      }

      function showAdminOverlay() {
        adminOverlay.classList.add("active");
        landingContent.style.filter = "blur(2px)";
        dotWave.style.filter = "blur(2px)";
      }

      function hideAdminOverlay() {
        adminOverlay.classList.remove("active");
        landingContent.style.filter = "none";
        dotWave.style.filter = "none";
        adminLogin.style.display = "flex";
        adminEditor.style.display = "none";
        adminStatus.textContent = "";
        adminStatusLoggedOut.textContent = "";
        document.getElementById("adminPassword").value = "";
      }

      async function loadMaterials() {
        const resp = await fetch("/admin/materials");
        const data = await resp.json();
        if (!data.ok) {
          setStatus(data.error || "Unable to load materials.");
          return;
        }
        adminTableBody.innerHTML = "";
        data.materials.forEach((mat) => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${mat.name}</td>
            <td>${mat.unit}</td>
            <td>${mat.currency}</td>
            <td><input type="number" step="0.01" value="${mat.unit_cost}" data-name="${mat.name}" /></td>
            <td><button data-name="${mat.name}">Save</button></td>
          `;
          adminTableBody.appendChild(row);
        });
        adminTableBody.querySelectorAll("button").forEach((btn) => {
          btn.addEventListener("click", async (e) => {
            const name = e.target.getAttribute("data-name");
            const input = adminTableBody.querySelector(`input[data-name="${name}"]`);
            const unit_cost = input.value;
            const resp = await fetch("/admin/materials/update", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ name, unit_cost }),
            });
            const result = await resp.json();
            if (!result.ok) {
              setStatus(result.error || "Update failed.");
              return;
            }
            setStatus("Saved!");
          });
        });
      }

      document.querySelector(".nav-cta").addEventListener("click", (e) => {
        e.preventDefault();
        showAdminOverlay();
      });

      document.getElementById("adminLoginBtn").addEventListener("click", async () => {
        const password = document.getElementById("adminPassword").value;
        if (!password) {
          setStatus("Enter the admin password.");
          return;
        }
        const resp = await fetch("/admin/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ password }),
        });
        const data = await resp.json();
        if (!data.ok) {
          setStatus(data.error || "Login failed.");
          return;
        }
        adminLogin.style.display = "none";
        adminEditor.style.display = "block";
        loadMaterials();
      });

      document.getElementById("adminLogoutBtn").addEventListener("click", async () => {
        await fetch("/admin/logout", { method: "POST" });
        hideAdminOverlay();
      });
    </script>
    """
    return page_template("Bakery Quotation", body, show_header=False, body_class="landing-page")


@router.get("/chat", response_class=HTMLResponse)
def chat():
    # Render the chat UI shell.
    body = """
    <div class="chat">
      <div class="messages" id="messages"></div>
      <div class="chat-input">
        <textarea id="chatInput" placeholder="Ask for a quote or any question..."></textarea>
        <button id="sendBtn">Send</button>
      </div>
    </div>
    <script>
      const messagesEl = document.getElementById("messages");
      const inputEl = document.getElementById("chatInput");
      const sendBtn = document.getElementById("sendBtn");
      const history = [];
      addBubble("assistant", "Hi there! I can help you with a bakery quote. What would you like to order today?");
      messagesEl.scrollTop = messagesEl.scrollHeight;

      function addBubble(role, content) {
        const div = document.createElement("div");
        div.className = "bubble " + role;
        div.innerHTML = formatMessage(content);
        messagesEl.appendChild(div);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }

      function formatMessage(text) {
        const escaped = text
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;");
        const bolded = escaped.replace(/\*\*(.+?)\*\*/g, (_, inner) => {
          return "<strong>" + inner.replace(/\*\*/g, "") + "</strong>";
        });
        return bolded.replace(/\*\*/g, "");
      }

      function addQuoteLinks(quote) {
        const wrap = document.createElement("div");
        wrap.className = "quote-bubble";
        const pdfLink = quote.pdf_filename
          ? `<a class="btn-link" href="/download/${quote.pdf_filename}">PDF</a>`
          : "";
        wrap.innerHTML = `
          <div class="quote-card">
            <div class="quote-title">Quote ready</div>
            <div class="quote-meta">ID: ${quote.quote_id}</div>
            <div class="quote-meta">Total: ${quote.total} ${quote.currency}</div>
            <div class="quote-actions">
              <a class="btn-link" href="/download/${quote.md_filename}">Markdown</a>
              <a class="btn-link" href="/download/${quote.txt_filename}">Text</a>
              ${pdfLink}
            </div>
          </div>
        `;
        messagesEl.appendChild(wrap);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }

      async function sendMessage() {
        const text = inputEl.value.trim();
        if (!text) return;
        inputEl.value = "";
        history.push({ role: "user", content: text });
        addBubble("user", text);
        addBubble("assistant", "Thinking...");
        const thinking = messagesEl.lastChild;

        const resp = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: history })
        });
        const data = await resp.json();
        thinking.innerHTML = formatMessage(data.reply || "No response");
        history.push({ role: "assistant", content: thinking.textContent });
        if (data.quote) {
          addQuoteLinks(data.quote);
        }
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }

      sendBtn.addEventListener("click", sendMessage);
      inputEl.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          sendMessage();
        }
      });
    </script>
    """
    return page_template("Bakery Quotation Chat", body)
