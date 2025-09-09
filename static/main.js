const api = {
  contestants: async () => fetch('/api/contestants').then(r => r.json()),
  submissions: async () => fetch('/api/submissions').then(r => r.json()),
  submit: async (payload) => fetch('/api/submissions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }).then(async r => {
    if (!r.ok) throw new Error((await r.json()).detail || 'Submission failed');
    return r.json();
  })
};

const contestantsContainer = document.getElementById('contestants');
const submissionsContainer = document.getElementById('submissions');
const form = document.getElementById('draft-form');
const message = document.getElementById('message');

function renderContestants(contestants) {
  contestantsContainer.innerHTML = '';
  for (const c of contestants) {
    const label = document.createElement('label');
    label.className = 'pill';
    label.innerHTML = `<input type="checkbox" value="${c.id}"> <span>${c.name}</span>`;
    contestantsContainer.appendChild(label);
  }
}

function renderSubmissions(submissions, contestants) {
  const idToName = new Map(contestants.map(c => [c.id, c.name]));
  submissionsContainer.innerHTML = '';
  for (const s of submissions) {
    const div = document.createElement('div');
    div.className = 'card';
    const picks = s.picks.map(id => idToName.get(id) || id).join(', ');
    div.innerHTML = `<strong>${s.display_name}</strong> <span class="muted">(${new Date(s.created_at || Date.now()).toLocaleString()})</span><div class="muted">${s.email || ''}</div><div>${picks}</div>`;
    submissionsContainer.appendChild(div);
  }
}

async function load() {
  const [contestants, submissions] = await Promise.all([
    api.contestants(),
    api.submissions(),
  ]);
  renderContestants(contestants);
  renderSubmissions(submissions, contestants);
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  message.textContent = '';
  const displayName = document.getElementById('displayName').value.trim();
  const email = document.getElementById('email').value.trim();
  const picks = Array.from(contestantsContainer.querySelectorAll('input[type="checkbox"]:checked')).map(cb => Number(cb.value));
  if (picks.length < 3) {
    message.textContent = 'Please select at least 3 contestants.';
    return;
  }
  const payload = { display_name: displayName, email: email || null, picks };
  try {
    form.querySelector('button').disabled = true;
    await api.submit(payload);
    form.reset();
    await load();
    message.textContent = 'Draft submitted!';
  } catch (err) {
    message.textContent = err.message || String(err);
  } finally {
    form.querySelector('button').disabled = false;
  }
});

load().catch(err => { message.textContent = String(err); });
