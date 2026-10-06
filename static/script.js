const source = document.getElementById('sourceCode');
const compileBtn = document.getElementById('compileBtn');
const sampleBtn = document.getElementById('sampleBtn');

sampleBtn.addEventListener('click', () => {
    source.value = sampleCode;
});

compileBtn.addEventListener('click', async () => {
    compileBtn.disabled = true;
    compileBtn.textContent = 'Compiling...';
    try {
        const response = await fetch('/compile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({source: source.value})
        });
        const data = await response.json();
        render(data);
    } catch (err) {
        document.getElementById('errors').textContent = `Request failed: ${err}`;
    } finally {
        compileBtn.disabled = false;
        compileBtn.textContent = 'Compile';
    }
});

function render(data) {
    for (const [key, value] of Object.entries(data.phases)) {
        const card = document.getElementById(`phase-${key}`);
        const span = card.querySelector('span');
        card.classList.remove('pass', 'fail');
        span.textContent = value;
        if (value === 'PASS') card.classList.add('pass');
        if (value === 'FAIL') card.classList.add('fail');
    }

    const tokenBody = document.querySelector('#tokenTable tbody');
    tokenBody.innerHTML = '';
    for (const token of data.tokens) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${escapeHtml(token.lexeme)}</td><td>${escapeHtml(token.token)}</td><td>${token.line}</td><td>${token.column}</td>`;
        tokenBody.appendChild(row);
    }

    const symbolBody = document.querySelector('#symbolTable tbody');
    symbolBody.innerHTML = '';
    for (const s of data.symbol_table) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${escapeHtml(s.name)}</td><td>${escapeHtml(s.type)}</td><td>${escapeHtml(s.scope)}</td><td>${s.line || '-'}</td>`;
        symbolBody.appendChild(row);
    }

    const errors = document.getElementById('errors');
    if (!data.errors.length) {
        errors.textContent = data.success ? 'No errors detected. Compilation successful.' : 'No errors reported.';
    } else {
        errors.innerHTML = data.errors.map(e =>
            `<div class="error-item"><span class="error-phase">${escapeHtml(e.phase)}</span>Line ${e.line || '-'}, Col ${e.column || '-'}: ${escapeHtml(e.message)}</div>`
        ).join('');
    }

    document.getElementById('astTree').textContent = data.ast_tree || 'AST not available.';
    document.getElementById('tac').textContent = data.tac.length ? data.tac.join('\n') : 'Intermediate code not generated.';
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}
