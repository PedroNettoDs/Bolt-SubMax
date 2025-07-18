/**
 * Módulo para gerenciamento da interface do usuário
 * Responsável por notificações, modais e interações gerais
 */
const UIManager = {
  
  /**
   * Exibe notificação para o usuário
   * @param {string} message - Mensagem a ser exibida
   * @param {string} type - Tipo da notificação (success, error, info)
   */
  showNotification(message, type = 'info') {
    // Remove notificações existentes
    document.querySelectorAll('.notification').forEach(el => el.remove());
    
    // Cria nova notificação
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    notification.innerHTML = `
      <div class="d-flex align-items-center justify-content-between">
        <div>
          <i class="bi ${type === 'success' ? 'bi-check-circle' : 'bi-exclamation-triangle'} me-2"></i>
          ${message}
        </div>
        <button type="button" class="btn-close ms-3" onclick="this.parentNode.parentNode.remove()" 
                style="background: none; border: none; font-size: 18px; cursor: pointer;">&times;</button>
      </div>
    `;
    
    document.body.appendChild(notification);
    
    // Anima entrada
    setTimeout(() => {
      notification.classList.add('show');
    }, 100);
    
    // Remove automaticamente após 5 segundos
    setTimeout(() => {
      notification.style.opacity = '0';
      notification.style.transform = 'translateX(100%)';
      
      setTimeout(() => {
        notification.remove();
      }, 300);
    }, 5000);
  },

  /**
   * Mostra input para nova série
   */
  showNewSeriesInput() {
    document.getElementById('liAdicionarSerie').classList.add('d-none');
    document.getElementById('liInputSerie').classList.remove('d-none');
    document.getElementById('inputNomeSerie').focus();
  },

  /**
   * Esconde input para nova série
   */
  hideNewSeriesInput() {
    document.getElementById('liInputSerie').classList.add('d-none');
    document.getElementById('liAdicionarSerie').classList.remove('d-none');
  },

  /**
   * Limpa o modal de treino
   */
  clearWorkoutModal() {
    console.log('Limpando modal de treino...');
    
    // Limpa todas as abas
    document.getElementById('conteudoTreinos').innerHTML = '';
    document.querySelectorAll('#abasTreino .nav-item:not(#liAdicionarSerie):not(#liInputSerie)')
      .forEach(el => el.remove());
    
    // Limpa campos
    document.getElementById('nomeTreino').value = '';
    document.getElementById('dataInicio').value = '';
    document.getElementById('anotacoes').value = '';
    
    // Esconde input de nova série
    this.hideNewSeriesInput();
  },

  /**
   * Inicializa o modal de treino
   */
  initWorkoutModal() {
    console.log('Modal de treino aberto, verificando cache...');
    
    // Verifica se o cache está carregado
    if (!ExerciseManager.cache) {
      ExerciseManager.loadExercises();
    }
    
    // Define data padrão como hoje
    const startDateInput = document.getElementById('dataInicio');
    if (startDateInput && !startDateInput.value) {
      startDateInput.value = new Date().toISOString().split('T')[0];
    }
    
    // Cria primeira aba se não existir nenhuma
    const existingTabs = document.querySelectorAll('#abasTreino .nav-item:not(#liAdicionarSerie):not(#liInputSerie)');
    if (existingTabs.length === 0) {
      WorkoutManager.addWorkoutTab('Série A');
    }
  },

  /**
   * Configura event listeners para inputs de nova série
   */
  setupNewSeriesInput() {
    const inputSeries = document.getElementById('inputNomeSerie');
    if (inputSeries) {
      inputSeries.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const name = inputSeries.value.trim();
          if (name) {
            WorkoutManager.addWorkoutTab(name);
          }
          inputSeries.value = '';
          this.hideNewSeriesInput();
        }
        if (e.key === 'Escape') {
          inputSeries.value = '';
          this.hideNewSeriesInput();
        }
      });
    }
  },

  /**
   * Configura sortable para as abas
   */
  setupSortableTabs() {
    const tabsContainer = document.getElementById('abasTreino');
    if (tabsContainer && typeof Sortable !== 'undefined') {
      new Sortable(tabsContainer, {
        filter: '#liAdicionarSerie,#liInputSerie',
        draggable: '.nav-item:not(#liAdicionarSerie):not(#liInputSerie)',
        animation: 150
      });
    }
  },

  /**
   * Configura listeners para modais
   */
  setupModalListeners() {
    // Modal de treino
    const workoutModal = document.getElementById('treinoModal');
    if (workoutModal) {
      workoutModal.addEventListener('shown.bs.modal', () => {
        this.initWorkoutModal();
      });
      
      workoutModal.addEventListener('hidden.bs.modal', () => {
        this.clearWorkoutModal();
      });
    }

    // Modal de cadastro de exercício
    const exerciseModal = document.getElementById('modalCadExercicio');
    if (exerciseModal) {
      exerciseModal.addEventListener('hidden.bs.modal', () => {
        console.log('Modal de cadastro fechado, recarregando exercícios...');
        setTimeout(() => {
          ExerciseManager.reloadCache();
        }, 500);
      });
    }

    // Formulário de cadastro de exercício
    const exerciseForm = document.getElementById('formCadastrarExercicio');
    if (exerciseForm) {
      exerciseForm.addEventListener('submit', () => {
        console.log('Formulário de exercício submetido');
      });
    }
  },

  /**
   * Configura botões principais
   */
  setupMainButtons() {
    // Botão de nova série
    const newSeriesBtn = document.getElementById('btnNovaSerie');
    if (newSeriesBtn) {
      newSeriesBtn.addEventListener('click', () => {
        this.showNewSeriesInput();
      });
    }

    // Botão de salvar treino
    const saveWorkoutBtn = document.getElementById('btnSalvarTreino');
    if (saveWorkoutBtn) {
      saveWorkoutBtn.addEventListener('click', () => {
        WorkoutManager.saveWorkout();
      });
    }

    // Botão de aplicar edição em massa
    const applyMassEditBtn = document.getElementById('btnAplicarEdicaoMassa');
    if (applyMassEditBtn) {
      applyMassEditBtn.addEventListener('click', () => {
        WorkoutManager.applyMassEdit();
      });
    }
  },

  /**
   * Verifica dependências necessárias
   * @returns {boolean}
   */
  checkDependencies() {
    if (typeof $ === 'undefined') {
      console.error('jQuery não está carregado!');
      this.showNotification('Erro: jQuery não está disponível', 'error');
      return false;
    }
    
    if (typeof $.fn.select2 === 'undefined') {
      console.error('Select2 não está carregado!');
      this.showNotification('Erro: Select2 não está disponível', 'error');
      return false;
    }
    
    console.log('Todas as dependências carregadas');
    return true;
  },

  /**
   * Inicializa todos os componentes da UI
   */
  async init() {
    console.log('Inicializando sistema de gerenciamento de exercícios...');
    
    // Verifica dependências
    if (!this.checkDependencies()) {
      return;
    }

    try {
      // Carrega o gráfico corporal
      await BodyGraphManager.loadGraph();
      
      // Carrega o cache de exercícios
      await ExerciseManager.loadExercises();

      // Configura componentes da UI
      this.setupNewSeriesInput();
      this.setupSortableTabs();
      this.setupModalListeners();
      this.setupMainButtons();
      
      // Inicializa event listeners do gráfico corporal
      BodyGraphManager.initEventListeners();

      console.log('Sistema inicializado com sucesso');
      
    } catch (error) {
      console.error('Erro na inicialização:', error);
      this.showNotification('Erro ao inicializar o sistema', 'error');
    }
  }
};

// Exporta para uso global
window.UIManager = UIManager;

