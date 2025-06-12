(function() {
  // conversion factors relative to meters
  const factors = {
    millimeter: 0.001,
    centimeter: 0.01,
    meter: 1,
    kilometer: 1000,
    inch: 0.0254,
    foot: 0.3048,
    yard: 0.9144,
    mile: 1609.344
  };

  const inp = document.getElementById('input-value');
  const out = document.getElementById('output-value');
  const fromSel = document.getElementById('unit-from');
  const toSel = document.getElementById('unit-to');
  const precisionCheckbox = document.getElementById('precision-toggle');
  const historyList = document.querySelector('.history-list');
  const clearBtn = document.querySelector('.clear-history');
  const formulaEl = document.getElementById('formula-text');
  const scaleContainer = document.querySelector('.scale-container');
  const linkFrom = document.getElementById('link-from');
  const linkTo = document.getElementById('link-to');

  let history = [];

  // generate scale ticks
  const ticksContainer = document.createElement('div');
  ticksContainer.className = 'ticks';
  for (let i = -20; i <= 20; i++) {
    const tick = document.createElement('div');
    tick.className = 'tick';
    ticksContainer.appendChild(tick);
  }
  scaleContainer.appendChild(ticksContainer);

  // capitalize first letter
  function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  // update wiki links based on units
  function updateLinks() {
    const fromName = capitalize(fromSel.value);
    const toName = capitalize(toSel.value);
    linkFrom.textContent = `Learn more about ${fromName}`;
    linkFrom.href = `https://en.wikipedia.org/wiki/${fromName}`;
    linkTo.textContent = `Learn more about ${toName}`;
    linkTo.href = `https://en.wikipedia.org/wiki/${toName}`;
  }

  // initial links
  updateLinks();

  function convertAndRecord() {
    const v = parseFloat(inp.value);
    if (isNaN(v)) {
      out.value = '';
      formulaEl.innerHTML = '<span class="highlight">Formula</span> — for any two units, value × (fromFactor ÷ toFactor)';
      updateLinks();
      return;
    }
    const fFrom = factors[fromSel.value];
    const fTo = factors[toSel.value];
    const raw = v * (fFrom / fTo);
    const display = precisionCheckbox.checked
      ? raw.toString()
      : raw.toFixed(3);

    out.value = display;

    // update dynamic formula
    formulaEl.textContent = `Formula — ${v} × (${fFrom} ÷ ${fTo}) = ${display}`;

    // animate scale divisions
    const offset = raw * 10; // 10px per unit
    ticksContainer.style.transform = `translate(-50%, calc(-50% - ${offset}px))`;

    // update links
    updateLinks();

    // push into history
    history.unshift({from: v, fromU: fromSel.options[fromSel.selectedIndex].text, to: display, toU: toSel.options[toSel.selectedIndex].text});
    if (history.length > 20) history.pop();
    renderHistory();
  }

  function renderHistory() {
    historyList.innerHTML = history.map(h => `<li>${h.from} ${h.fromU} → ${h.to} ${h.toU}</li>`).join('');
  }

  // wire up events
  [inp, fromSel, toSel, precisionCheckbox].forEach(el => el.addEventListener('input', convertAndRecord));
  clearBtn.addEventListener('click', () => { history = []; renderHistory(); });
})();
