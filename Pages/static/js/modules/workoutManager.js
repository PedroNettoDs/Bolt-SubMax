/**
 * Módulo para gerenciamento de treinos
 * Responsável por salvar, validar e manipular dados de treinos
 */
const WorkoutManager = {
  selectedRows: [],

  /**
   * Salva o treino via API REST
   */
  async saveWorkout() {
    console.log('Iniciando salvamento do treino via REST API...');
    
    const btnSave = document.getElementById('btnSalvarTreino');
    const originalText = btnSave.innerHTML;
    
    try {
      // Feedback visual
      btnSave.disabled = true;
      btnSave.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Salvando...';
      
      // Validação e coleta de dados
      const workoutData = await this.collectWorkoutData();
      
      if (!workoutData.exercicios || workoutData.exercicios.length === 0) {
        throw new Error('Adicione pelo menos um exercício ao treino');
      }

      console.log('Enviando dados para API:', workoutData);

      // Envia via REST API
      const response = await fetch('/api/treinos-aluno/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken()
        },
        body: JSON.stringify(workoutData)
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('Erro da API:', errorData);
        throw new Error(errorData.detail || errorData.message || `Erro HTTP: ${response.status}`);
      }

      const result = await response.json();
      
      console.log('Treino salvo com sucesso via API:', result);
      
      // Fecha o modal
      bootstrap.Modal.getInstance(document.getElementById('treinoModal')).hide();
      
      // Recarrega a aba de treinos
      await this.reloadWorkoutsTab();
      
      // Feedback de sucesso
      UIManager.showNotification(
        `Treino "${result.nome}" salvo com sucesso!`, 
        'success'
      );
      
    } catch (error) {
      console.error('Erro ao salvar treino:', error);
      UIManager.showNotification(`Erro ao salvar treino: ${error.message}`, 'error');
    } finally {
      // Restaura botão
      btnSave.disabled = false;
      btnSave.innerHTML = originalText;
    }
  },

  /**
   * Coleta dados do treino no formato da API
   * @returns {Promise<Object>}
   */
  async collectWorkoutData() {
    const name = document.getElementById('nomeTreino').value.trim();
    const startDate = document.getElementById('dataInicio').value;
    const notes = document.getElementById('anotacoes').value.trim();

    if (!name) throw new Error('O nome do treino é obrigatório');
    if (!startDate) throw new Error('A data de início é obrigatória');

    const exercisesBySeries = [];

    // Seleciona todas as séries (abas)
    const tabs = document.querySelectorAll('#abasTreino .nav-link');
    for (let i = 0; i < tabs.length; i++) {
      const tab = tabs[i];
      const seriesId = tab.getAttribute('href')?.replace('#', '');
      const seriesName = tab.textContent.trim();
      if (!seriesId || !seriesName) continue;

      const tabPane = document.getElementById(seriesId);
      if (!tabPane) continue;

      const exercises = [];
      const rows = tabPane.querySelectorAll('.exercicio-row');
      
      for (const row of rows) {
        const $select = $(row).find('.select-exercicio');
        if (!$select.hasClass('select2-hidden-accessible')) continue;

        const exerciseData = $select.select2('data')[0];
        if (!exerciseData) continue;

        const weight = parseFloat(row.querySelector('[data-field="carga"] input')?.value) || 0;
        const reps = parseInt(row.querySelector('[data-field="repsDesejadas"] input')?.value) || 0;
        const sets = parseInt(row.querySelector('[data-field="sets"] input')?.value) || 0;
        const rest = parseInt(row.querySelector('[data-field="descanso"] input')?.value) || 0;
        const method = row.querySelector('[data-field="metodo"] select')?.value || 'tradicional';
        const exerciseNotes = row.nextElementSibling?.querySelector('[data-field="notas"]')?.value?.trim() || '';

        exercises.push({
          nome: exerciseData.nome,
          series: sets,
          repeticoes: reps,
          carga: weight,
          intervalo_seg: rest,
          metodo: method,
          notas: exerciseNotes
        });
      }

      // Apenas adiciona a série se houver exercícios
      if (exercises.length > 0) {
        exercisesBySeries.push({
          serie: seriesName,
          ordem: i + 1,
          exercicios: exercises
        });
      }
    }

    const studentId = this.getStudentId();
    if (!studentId) throw new Error('ID do aluno não encontrado');

    return {
      aluno: studentId,
      nome: name,
      data_inicio: startDate,
      observacoes: notes,
      exercicios: exercisesBySeries
    };
  },

  /**
   * Obtém o ID do aluno
   * @returns {number|null}
   */
  getStudentId() {
    // Tenta obter da URL
    const urlPath = window.location.pathname;
    const match = urlPath.match(/\/aluno\/(\d+)/);
    if (match && match[1]) {
      return parseInt(match[1]);
    }
    
    // Tenta obter de uma variável global
    if (window.alunoId) {
      return window.alunoId;
    }
    
    // Tenta obter de um elemento na página
    const studentIdElement = document.querySelector('[data-aluno-id]');
    if (studentIdElement) {
      return parseInt(studentIdElement.dataset.alunoId);
    }
    
    console.warn('ID do aluno não encontrado');
    return null;
  },

  /**
   * Obtém o token CSRF
   * @returns {string}
   */
  getCSRFToken() {
    // Tenta obter do cookie
    const cookieValue = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    
    if (cookieValue) return cookieValue;
    
    // Tenta obter de um campo oculto
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) return csrfInput.value;
    
    // Tenta obter do meta tag
    const csrfMeta = document.querySelector('meta[name="csrf-token"]');
    if (csrfMeta) return csrfMeta.getAttribute('content');
    
    console.warn('CSRF token não encontrado');
    return '';
  },

  /**
   * Recarrega a aba de treinos
   */
  async reloadWorkoutsTab() {
    console.log('Recarregando aba de treinos...');
    
    try {
      const studentId = this.getStudentId();
      if (!studentId) {
        console.warn('ID do aluno não encontrado para recarregar treinos');
        return;
      }

      const response = await fetch(`/aluno/${studentId}/treinos/`);
      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const html = await response.text();
      
      // Atualiza o conteúdo da aba de treinos
      const workoutsTab = document.querySelector('#treinos');
      if (workoutsTab) {
        workoutsTab.innerHTML = html;
        console.log('Aba de treinos recarregada');
        
        // Inicializa quaisquer scripts necessários na aba
        if (typeof initTreinosTab === 'function') {
          initTreinosTab();
        }
      } else {
        console.warn('Aba de treinos não encontrada');
      }
      
    } catch (error) {
      console.error('Erro ao recarregar aba de treinos:', error);
      UIManager.showNotification('Não foi possível atualizar a lista de treinos', 'error');
    }
  },

  /**
   * Adiciona um novo exercício à tabela
   * @param {string} workoutId - ID do treino
   */
  addExercise(workoutId) {
    console.log('Adicionando exercício para treino:', workoutId);
    
    const table = document.getElementById(`tabelaExercicios_${workoutId}`);
    if (!table) {
      console.error('Tabela não encontrada:', `tabelaExercicios_${workoutId}`);
      return;
    }
    
    const uid = Math.random().toString(36).slice(2,7);
    const selectId = `select_exercicio_${uid}`;

    const mainRow = this.createExerciseRow(uid, selectId);
    const detailsRow = this.createDetailsRow(uid);

    table.insertAdjacentHTML('beforeend', mainRow + detailsRow);
    const rowElement = document.getElementById(`row_${uid}`);
    
    // Configura o Select2 para o novo select de exercício
    const $selectExercise = $(`#${selectId}`);
    
    // Aguarda um pouco para o DOM estar pronto
    setTimeout(() => {
      if (typeof $ !== 'undefined' && typeof $.fn.select2 !== 'undefined') {
        ExerciseManager.configureSelect2($selectExercise);
      } else {
        console.error('jQuery ou Select2 não disponível');
      }
    }, 100);
    
    // Adiciona listeners para outros campos
    this.setupRowEventListeners(rowElement);
    
    // Configura "Select All" checkbox
    this.setupSelectAllCheckbox(workoutId, table);
  },

  /**
   * Cria HTML para linha principal do exercício
   * @param {string} uid - ID único
   * @param {string} selectId - ID do select
   * @returns {string}
   */
  createExerciseRow(uid, selectId) {
    return `
      <tr class="exercicio-row" id="row_${uid}">
        <td class="text-center"><input class="form-check-input mass-check" type="checkbox"></td>
        <td data-field="nome">
          <select id="${selectId}" class="form-select select-exercicio" style="width: 100%;">
            <option></option>
          </select>
        </td>
        <td data-field="carga"><input class="form-control" type="number" placeholder="kg" step="0.1"></td>
        <td data-field="repsDesejadas"><input class="form-control" type="number" placeholder="reps"></td>
        <td data-field="sets"><input class="form-control" type="number" min="1" placeholder="sets"></td>
        <td data-field="descanso"><input class="form-control" type="number" placeholder="seg"></td>
        <td data-field="metodo">
          <select class="form-select" onchange="WorkoutManager.handleMethodChange(this)">
            <option value="">Tradicional</option>
            <option value="drop_set">Drop Set</option>
            <option value="bi_set">Superset / Bi-set</option>
            <option value="rest_pause">Rest Pause</option>
            <option value="piramidal">Piramidal</option>
            <option value="negativa">Negativa</option>
          </select>
        </td>
      </tr>`;
  },

  /**
   * Cria HTML para linha de detalhes
   * @param {string} uid - ID único
   * @returns {string}
   */
  createDetailsRow(uid) {
    return `
      <tr class="detalhes-row d-none" data-parent="row_${uid}">
        <td colspan="7"><input class="form-control" data-field="notas" placeholder="Notas / Resultado"></td>
      </tr>`;
  },

  /**
   * Configura event listeners para uma linha
   * @param {HTMLElement} mainRow - Elemento da linha principal
   */
  setupRowEventListeners(mainRow) {
    mainRow.querySelectorAll('input, select:not(.select-exercicio)').forEach(el => {
      el.addEventListener('input', () => this.recalculateRow(mainRow));
      el.addEventListener('change', () => this.recalculateRow(mainRow));
    });
    
    // Configura checkbox para seleção em massa
    const checkbox = mainRow.querySelector('.mass-check');
    if (checkbox) {
      checkbox.addEventListener('change', function() {
        mainRow.classList.toggle('table-active', this.checked);
      });
    }
  },

  /**
   * Configura checkbox "Select All"
   * @param {string} workoutId - ID do treino
   * @param {HTMLElement} table - Elemento da tabela
   */
  setupSelectAllCheckbox(workoutId, table) {
    const selectAllCheckbox = document.getElementById(`selectAll_${workoutId}`);
    if (selectAllCheckbox) {
      selectAllCheckbox.addEventListener('change', function() {
        const isChecked = this.checked;
        table.querySelectorAll('.mass-check').forEach(cb => {
          cb.checked = isChecked;
          cb.dispatchEvent(new Event('change'));
        });
      });
    }
  },

  /**
   * Manipula mudança de método de treino
   * @param {HTMLElement} selectEl - Elemento select
   */
  handleMethodChange(selectEl) {
    const method = selectEl.value;
    const mainRow = selectEl.closest('tr.exercicio-row');
    const detailsRow = mainRow.nextElementSibling;
    
    if (!method) { 
      detailsRow.classList.add('d-none'); 
      return; 
    }
    
    detailsRow.classList.remove('d-none');
    this.recalculateRow(mainRow);
  },

  /**
   * Recalcula valores da linha baseado no método
   * @param {HTMLElement} mainRow - Linha principal
   */
  recalculateRow(mainRow) {
    const method = mainRow.querySelector('[data-field="metodo"] select').value;
    const detailsRow = mainRow.nextElementSibling;
    const notesInput = detailsRow.querySelector('[data-field="notas"]');
    
    if (!method) { 
      notesInput.value = ''; 
      return; 
    }
    
    const weight = parseFloat(mainRow.querySelector('[data-field="carga"] input').value) || 0;
    const reps = parseInt(mainRow.querySelector('[data-field="repsDesejadas"] input').value) || 0;
    const sets = parseInt(mainRow.querySelector('[data-field="sets"] input').value) || 0;
    
    let result = '';
    
    switch (method) {
      case 'drop_set':
        result = this.calculateDropSet(weight, sets);
        break;
      case 'bi_set':
        result = this.calculateBiSet(weight, reps, sets);
        break;
      case 'rest_pause':
        result = this.calculateRestPause(reps);
        break;
      case 'piramidal':
        result = this.calculatePyramidal(weight, sets);
        break;
      case 'negativa':
        result = this.calculateNegative(weight);
        break;
    }
    
    notesInput.value = result;
  },

  /**
   * Calcula drop set
   */
  calculateDropSet(weight, sets) {
    if (!weight || !sets) return '';
    
    let currentWeight = weight;
    const decrement = weight / sets;
    const series = [];
    
    for (let i = 1; i <= sets && currentWeight > 0; i++) {
      series.push(`S${i}: ${currentWeight.toFixed(1)}kg`);
      currentWeight = Math.max(0, currentWeight - decrement);
    }
    
    return series.join(', ');
  },

  /**
   * Calcula bi-set
   */
  calculateBiSet(weight, reps, sets) {
    if (!weight || !reps || !sets) return '';
    
    const volume = weight * reps * sets;
    return `Volume total: ${volume.toFixed(1)} kg•rep`;
  },

  /**
   * Calcula rest pause
   */
  calculateRestPause(reps) {
    if (!reps) return '';
    
    const miniSets = Math.ceil(reps / 3);
    const repsPerSet = Math.ceil(reps / miniSets);
    return `${miniSets} mini-sets de ~${repsPerSet} reps`;
  },

  /**
   * Calcula piramidal
   */
  calculatePyramidal(weight, sets) {
    if (!weight || !sets) return '';
    
    const series = [];
    for (let i = 1; i <= sets; i++) {
      const percentage = 50 + (50 * (i - 1) / (sets - 1));
      const setWeight = (weight * percentage / 100).toFixed(1);
      series.push(`S${i}: ${setWeight}kg`);
    }
    return series.join(', ');
  },

  /**
   * Calcula negativa
   */
  calculateNegative(weight) {
    if (!weight) return '';
    
    const eccentricWeight = (weight * 1.25).toFixed(1);
    return `Fase excêntrica: ${eccentricWeight}kg`;
  },

  /**
   * Adiciona nova aba de treino
   * @param {string} name - Nome da série
   */
  addWorkoutTab(name) {
    if (!name) return;
    
    // Sanitiza o nome
    const sanitizedName = name.trim();
    if (sanitizedName.length === 0) {
      UIManager.showNotification('O nome da série não pode estar vazio', 'error');
      return;
    }
    
    const id = 'treino_' + Math.random().toString(36).slice(2,7);
    
    // Verifica se já existe uma aba com esse nome
    const existingTabs = Array.from(document.querySelectorAll('#abasTreino .nav-link'))
      .map(el => el.textContent.trim());
    
    if (existingTabs.includes(sanitizedName)) {
      UIManager.showNotification(`Já existe uma série chamada "${sanitizedName}"`, 'error');
      return;
    }
    
    const tabHTML = `
      <li class="nav-item">
        <a class="nav-link" data-bs-toggle="tab" href="#${id}" role="tab">
          ${sanitizedName}
        </a>
      </li>`;
    
    document.getElementById('abasTreino').insertAdjacentHTML('beforeend', tabHTML);

    const contentHTML = this.createTabContent(id);
    document.getElementById('conteudoTreinos').insertAdjacentHTML('beforeend', contentHTML);
    
    // Ativa a nova aba
    new bootstrap.Tab(document.querySelector(`a[href="#${id}"]`)).show();
    
    // Adiciona primeiro exercício automaticamente
    setTimeout(() => {
      this.addExercise(id);
    }, 100);
  },

  /**
   * Cria conteúdo da aba
   * @param {string} id - ID da aba
   * @returns {string}
   */
  createTabContent(id) {
    return `
      <div class="tab-pane fade" id="${id}" role="tabpanel">
        <div class="table-responsive">
          <table class="table table-bordered align-middle small w-100">
            <thead class="table-light">
              <tr>
                <th style="width: 40px;">
                  <input type="checkbox" class="form-check-input" id="selectAll_${id}">
                </th>
                <th>Exercício</th>
                <th style="width: 100px;">Carga (kg)</th>
                <th style="width: 100px;">Reps</th>
                <th style="width: 80px;">Sets</th>
                <th style="width: 100px;">Descanso (s)</th>
                <th>
                  Método 
                  <button class="btn btn-sm btn-outline-primary ms-2" onclick="WorkoutManager.openMassEdit('${id}')">
                    <i class="bi bi-pencil-square me-1"></i>Edição em massa
                  </button>
                </th>
              </tr>
            </thead>
            <tbody id="tabelaExercicios_${id}"></tbody>
          </table>
          <button class="btn btn-outline-secondary btn-sm mt-2" onclick="WorkoutManager.addExercise('${id}')">
            <i class="bi bi-plus-circle me-1"></i>Adicionar exercício
          </button>
        </div>
      </div>`;
  },

  /**
   * Abre modal de edição em massa
   * @param {string} workoutId - ID do treino
   */
  openMassEdit(workoutId) {
    const rows = document.querySelectorAll(`#tabelaExercicios_${workoutId} tr.exercicio-row`);
    this.selectedRows = Array.from(rows).filter(r => r.querySelector('input[type="checkbox"]')?.checked);
    
    if (!this.selectedRows.length) {
      UIManager.showNotification('Selecione pelo menos um exercício para edição em massa', 'error');
      return;
    }
    
    document.getElementById('formEdicaoMassa').reset();
    new bootstrap.Modal(document.getElementById('edicaoMassaModal')).show();
  },

  /**
   * Aplica edição em massa
   */
  applyMassEdit() {
    const fields = [
      {k: 'carga', id: 'massa_carga'},
      {k: 'repsDesejadas', id: 'massa_repsDesejadas'},
      {k: 'sets', id: 'massa_sets'},
      {k: 'descanso', id: 'massa_descanso'}
    ];
    
    const newValues = {};
    fields.forEach(({k, id}) => {
      const value = document.getElementById(id).value.trim();
      if (value) newValues[k] = value;
    });
    
    if (Object.keys(newValues).length === 0) {
      UIManager.showNotification('Preencha pelo menos um campo para aplicar', 'error');
      return;
    }
    
    // Aplica os novos valores
    this.selectedRows.forEach(row => {
      Object.entries(newValues).forEach(([field, value]) => {
        const input = row.querySelector(`[data-field="${field}"] input`);
        if (input) {
          input.value = value;
          input.dispatchEvent(new Event('change'));
        }
      });
      
      this.recalculateRow(row);
    });
    
    bootstrap.Modal.getInstance(document.getElementById('edicaoMassaModal')).hide();
    UIManager.showNotification(`Alterações aplicadas em ${this.selectedRows.length} exercício(s)`, 'success');
  }
};

// Exporta para uso global
window.WorkoutManager = WorkoutManager;

