<script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>

/* ---------- Configurações ---------- */
const metodoConfig = {
  "":                 [],
  "drop_set":         [],
  "bi_set":           [],
  "rest_pause":       [],
  "piramidal":        [],
  "negativa":         []
};

/* ---------- Manipulação de Método ---------- */
function handleMetodoChange(selectEl) {
  const metodo = selectEl.value;
  const mainRow = selectEl.closest("tr.exercicio-row");
  const detalhesRow = mainRow.nextElementSibling;

  if (metodo === "") {
    detalhesRow.classList.add("d-none");
    return;
  }
  detalhesRow.classList.remove("d-none");
  recalcularLinha(mainRow);
}

/* ---------- CRUD de linhas ---------- */
function adicionarExercicio(treinoId) {
  const tabela = document.getElementById(`tabelaExercicios_${treinoId}`);
  const uid = Math.random().toString(36).substring(2, 7);

  const linhaPrincipal = `
    <tr class="exercicio-row" id="row_${uid}">
      <td data-field="nome">
        <input class="form-check-input me-2" type="checkbox">
        <input class="form-control d-inline-block w-75" placeholder="Pesquisar exercício">
      </td>
      <td data-field="carga"><input class="form-control" type="number" placeholder="kg" step="0.1"></td>
      <td data-field="repsDesejadas"><input class="form-control" type="number"></td>
      <td data-field="sets"><input class="form-control" type="number" min="1"></td>
      <td data-field="descanso"><input class="form-control" type="number" placeholder="seg"></td>
      <td data-field="metodo">
        <select class="form-select" onchange="handleMetodoChange(this)">
          <option value="">Tradicional</option>
          <option value="drop_set">Drop Set</option>
          <option value="bi_set">Superset / Bi-set</option>
          <option value="rest_pause">Rest Pause</option>
          <option value="piramidal">Piramidal</option>
          <option value="negativa">Negativa</option>
        </select>
      </td>
    </tr>`;

  const linhaDetalhes = `
    <tr class="detalhes-row d-none" data-parent="row_${uid}">
      <td colspan="6">
        <div class="row g-2">
          <div class="col-12" data-field="notas"><input class="form-control" placeholder="Notas / Resultado"></div>
        </div>
      </td>
    </tr>`;

  tabela.insertAdjacentHTML('beforeend', linhaPrincipal + linhaDetalhes);

  const mainRow = document.getElementById(`row_${uid}`);
  mainRow.querySelectorAll('input, select').forEach(el => {
    el.addEventListener('input', () => recalcularLinha(mainRow));
    el.addEventListener('change', () => recalcularLinha(mainRow));
  });
}

function adicionarAbaTreino(nome) {
  if (!nome) return;
  const id = 'treino_' + Math.random().toString(36).substring(2, 7);

  const abaHTML = `<li class="nav-item" role="presentation"><a class="nav-link" data-bs-toggle="tab" href="#${id}" role="tab">${nome}</a></li>`;
  document.getElementById('abasTreino').insertAdjacentHTML('beforeend', abaHTML);

  const conteudoHTML = `
    <div class="tab-pane fade" id="${id}" role="tabpanel">
      <div class="table-responsive">
        <table class="table table-bordered align-middle small w-100">
          <thead class="table-light">
            <tr>
              <th>Exercício</th>
              <th>Carga (kg)</th>
              <th>Reps desejadas</th>
              <th>Sets</th>
              <th>Descanso (s)</th>
              <th>Método <button class="btn btn-sm btn-outline-primary ms-2" onclick="abrirEdicaoEmMassa('${id}')">Edição em massa</button></th>
            </tr>
          </thead>
          <tbody id="tabelaExercicios_${id}"></tbody>
        </table>
        <button class="btn btn-outline-secondary btn-sm" onclick="adicionarExercicio('${id}')">+ Adicionar exercício</button>
      </div>
    </div>`;

  document.getElementById('conteudoTreinos').insertAdjacentHTML('beforeend', conteudoHTML);
  new bootstrap.Tab(document.querySelector(`a[href="#${id}"]`)).show();
}

/* ---------- Cálculos Automáticos ---------- */
function recalcularLinha(mainRow) {
  const metodo      = mainRow.querySelector('[data-field="metodo"] select').value;
  const detalhesRow = mainRow.nextElementSibling;
  const notasInput  = detalhesRow.querySelector('[data-field="notas"] input');
  if (!metodo) { notasInput.value = ''; return; }

  const carga = parseFloat(mainRow.querySelector('[data-field="carga"] input').value) || 0;
  const reps  = parseInt(mainRow.querySelector('[data-field="repsDesejadas"] input').value) || 0;
  const sets  = parseInt(mainRow.querySelector('[data-field="sets"] input').value) || 0;

  let resultado = '';
  switch (metodo) {
    case 'drop_set':
      if (carga && sets) {
        let cargaAtual = carga;
        const decremento = carga / sets;
        const series = [];
        for (let i = 1; i <= sets && cargaAtual > 0; i++) {
          series.push(`S${i}: ${cargaAtual.toFixed(1)}kg`);
          cargaAtual = Math.max(0, cargaAtual - decremento);
        }
        resultado = series.join(', ');
      }
      break;

    case 'bi_set':
      if (carga && reps && sets) {
        resultado = `Volume: ${(carga * reps * sets).toFixed(1)} kg•rep`;
      }
      break;

    case 'rest_pause':
      if (reps) {
        const miniSets = Math.ceil(reps / 3);
        resultado = `${miniSets} mini-sets ~${Math.ceil(reps / miniSets)} reps`;
      }
      break;

    case 'piramidal':
      if (carga && sets) {
        const series = [];
        for (let i = 1; i <= sets; i++) {
          const pct = 50 + (50 * (i - 1) / (sets - 1));
          series.push(`S${i}: ${(carga * pct / 100).toFixed(1)}kg`);
        }
        resultado = series.join(', ');
      }
      break;

    case 'negativa':
      if (carga) {
        resultado = `Excêntrica: ${(carga * 1.25).toFixed(1)}kg`;
      }
      break;
  }
  notasInput.value = resultado;
}

/* ---------- Edição em massa ---------- */
let linhasSelecionadas = [];
function abrirEdicaoEmMassa(treinoId) {
  const linhas = document.querySelectorAll(`#tabelaExercicios_${treinoId} tr.exercicio-row`);
  linhasSelecionadas = Array.from(linhas).filter(r => r.querySelector('input[type="checkbox"]').checked);
  if (linhasSelecionadas.length === 0) return alert('Selecione pelo menos um exercício.');

  document.getElementById('formEdicaoMassa').reset();
  const modal = new bootstrap.Modal(document.getElementById('edicaoMassaModal'));
  modal.show();
}

document.getElementById('btnAplicarEdicaoMassa').addEventListener('click', () => {
  const campos = [
    { chave: 'carga',       inputId: 'massa_carga' },
    { chave: 'repsDesejadas', inputId: 'massa_repsDesejadas' },
    { chave: 'sets',        inputId: 'massa_sets' },
    { chave: 'descanso',    inputId: 'massa_descanso' }
  ];
  const novosValores = {};
  campos.forEach(({ chave, inputId }) => {
    const val = document.getElementById(inputId).value.trim();
    if (val !== '') novosValores[chave] = val;
  });
  if (Object.keys(novosValores).length === 0) return alert('Nenhum valor informado.');

  linhasSelecionadas.forEach(mainRow => {
    const detailsRow = mainRow.nextElementSibling;
    Object.entries(novosValores).forEach(([chave, valor]) => {
      const el = mainRow.querySelector(`[data-field="${chave}"] input`);
      if (el) el.value = valor;
    });
    recalcularLinha(mainRow);
  });

  bootstrap.Modal.getInstance(document.getElementById('edicaoMassaModal')).hide();
});

/* ---------- UI util ---------- */
function mostrarInputNovaSerie() {
  document.getElementById('liAdicionarSerie').classList.add('d-none');
  document.getElementById('liInputSerie').classList.remove('d-none');
  document.getElementById('inputNomeSerie').focus();
}

document.addEventListener('DOMContentLoaded', () => {
  const inputSerie = document.getElementById('inputNomeSerie');
  inputSerie.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const nome = inputSerie.value.trim();
      if (nome) adicionarAbaTreino(nome);
      inputSerie.value = '';
      document.getElementById('liInputSerie').classList.add('d-none');
      document.getElementById('liAdicionarSerie').classList.remove('d-none');
    } else if (e.key === 'Escape') {
      inputSerie.value = '';
      document.getElementById('liInputSerie').classList.add('d-none');
      document.getElementById('liAdicionarSerie').classList.remove('d-none');
    }
  });

  new Sortable(document.getElementById('abasTreino'), {
    filter: '#liAdicionarSerie, #liInputSerie',
    draggable: '.nav-item:not(#liAdicionarSerie):not(#liInputSerie)',
    animation: 150
  });
});