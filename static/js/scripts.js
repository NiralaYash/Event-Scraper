async function loadEvents() {
  try {
    const res = await fetch('/api/events');
    const data = await res.json();
    const container = document.getElementById('events');
    container.innerHTML = '';

    data.forEach(event => {
      const card = document.createElement('div');
      card.className = 'event-card';

      card.innerHTML = `
        <img src="${event.image}" alt="Event Image"
        style="width: 100%; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 1rem; display: block;">

        <div style="flex-grow: 1; display: flex; flex-direction: column;">
          <div class="event-title">${event.title}</div>
          <div class="event-date">${event.date}</div>
          <div class="event-location">${event.location}</div>
        </div>
        <button class="btn" onclick="handleGetTickets('${event.link}')">GET TICKETS</button>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error('Failed to load events:', err);
  }
}

let currentLink = "";

function handleGetTickets(link) {
  currentLink = link;
  document.getElementById('emailInput').value = "";
  document.getElementById('emailModal').style.display = "flex";
}

async function submitEmail() {
  const email = document.getElementById('emailInput').value.trim();
  if (email && email.includes('@')) {
    try {
      await fetch('/log_email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, link: currentLink })
      });
    } catch (err) {
      console.warn("Failed to log email.");
    }
  }
  redirectToEvent();
}

function skipEmail() {
  redirectToEvent();
}

function redirectToEvent() {
  document.getElementById('emailModal').style.display = "none";
  window.location.href = currentLink;
}

window.addEventListener('load', loadEvents);
