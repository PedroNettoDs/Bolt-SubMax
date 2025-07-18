/**
 * Módulo para gerenciamento de exercícios
 * Responsável por carregar, filtrar e configurar exercícios
 */
const ExerciseManager = {
  cache: null,
  isLoading: false,

  /**
   * Carrega exercícios da API ou cache
   * @returns {Promise<Array>}
   */
  async loadExercises() {
    if (this.isLoading) {
      console.log('Carregamento já em andamento...');
      return this.cache || [];
    }

    console.log('Carregando exercícios...');
    
    // Verifica cache válido
    const cachedData = CacheManager.get();
    if (cachedData) {
      console.log('Exercícios carregados do cache:', cachedData.length);
      this.cache = cachedData;
      return this.cache;
    }

    // Busca da API
    this.isLoading = true;
    try {
      const response = await fetch('{% url "exercicios_json" %}?q=');
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      this.cache = data.results || [];
      
      // Salva no cache
      CacheManager.set(this.cache);
      
      console.log('Exercícios carregados da API:', this.cache.length);
      return this.cache;
      
    } catch (error) {
      console.error('Erro ao carregar exercícios:', error);
      UIManager.showNotification(`Erro ao carregar exercícios: ${error.message}`, 'error');
      return [];
    } finally {
      this.isLoading = false;
    }
  },

  /**
   * Filtra exercícios por termo de busca
   * @param {string} term - Termo de busca
   * @returns {Array}
   */
  filterExercises(term) {
    if (!this.cache) return [];
    if (!term || term.length < 2) return [];
    
    const termLower = term.toLowerCase();
    return this.cache
      .filter(ex => ex.nome.toLowerCase().includes(termLower))
      .slice(0, 20);
  },

  /**
   * Configura Select2 para um elemento de exercício
   * @param {jQuery} $select - Elemento select jQuery
   */
  configureSelect2($select) {
    console.log('Configurando Select2 para:', $select.attr('id') || 'select sem ID');
    
    // Destrói instância existente
    if ($select.hasClass('select2-hidden-accessible')) {
      $select.select2('destroy');
    }

    // Remove atributos conflitantes
    $select.removeAttr('aria-readonly readonly disabled');
    $select.prop('disabled', false);

    const config = {
      theme: 'bootstrap-5',
      placeholder: 'Digite para buscar exercício...',
      minimumInputLength: 2,
      allowClear: true,
      width: '100%',
      dropdownParent: $('#treinoModal'),
      ajax: {
        transport: (params, success, failure) => {
          const term = params.data.q || '';
          
          // Mostra loading
          const $container = $select.next('.select2-container');
          $container.addClass('select2-container--loading');
          
          setTimeout(() => {
            try {
              const results = this.filterExercises(term);
              
              success({
                results: results.map(item => ({
                  id: item.id,
                  text: item.nome,
                  nome: item.nome,
                  descricao: item.descricao || '',
                  categoria: item.categoria || '',
                  grupo_muscular: item.grupo_muscular || ''
                }))
              });
            } catch (error) {
              console.error('Erro na busca:', error);
              failure();
            } finally {
              $container.removeClass('select2-container--loading');
            }
          }, 150);
        },
        delay: 300,
        cache: true
      },
      language: {
        noResults: () => {
          return '<div class="select2-results__option select2-results__option--cadastrar-exercicio">' +
                 '<button type="button" class="btn-cadastrar-exercicio" onclick="ExerciseManager.openNewExerciseModal()">' +
                 '<i class="bi bi-plus-circle me-1"></i> Cadastrar novo exercício' +
                 '</button></div>';
        },
        inputTooShort: () => '<div class="text-muted p-2">Digite pelo menos 2 caracteres para buscar</div>',
        searching: () => '<div class="text-muted p-2"><span class="loading-spinner me-2"></span>Buscando exercícios...</div>',
        errorLoading: () => '<div class="text-danger p-2">Erro ao carregar exercícios</div>'
      },
      escapeMarkup: markup => markup
    };

    try {
      $select.select2(config);
      console.log('Select2 inicializado com sucesso');
      
      // Event listeners
      $select.on('select2:select', (e) => {
        const data = e.params.data;
        console.log('Exercício selecionado:', data.text);
        
        this.updateMuscleGroupDisplay($select, data);
        
        // Atualizar o gráfico corporal
        if (data.grupo_muscular) {
          BodyGraphManager.updateGraph(data.grupo_muscular);
        }
      });

      $select.on('select2:clear', () => {
        console.log('Exercício removido');
        this.updateMuscleGroupDisplay($select, null);
      });
      
    } catch (error) {
      console.error('Erro ao inicializar Select2:', error);
      UIManager.showNotification('Erro ao configurar busca de exercícios', 'error');
    }
  },

  /**
   * Atualiza a exibição do grupo muscular
   * @param {jQuery} $select - Elemento select
   * @param {Object|null} exerciseData - Dados do exercício
   */
  updateMuscleGroupDisplay($select, exerciseData) {
    const container = $select.closest('td');
    let groupInfo = container.find('.grupo-muscular-info');
    
    // Remove info existente
    groupInfo.remove();
    
    // Adiciona nova info se exercício foi selecionado
    if (exerciseData && exerciseData.grupo_muscular) {
      const formattedGroup = this.formatMuscleGroup(exerciseData.grupo_muscular);
      const groupHtml = `
        <div class="grupo-muscular-info">
          <i class="bi bi-tag-fill"></i>
          <span class="grupo-muscular-badge">${formattedGroup}</span>
        </div>`;
      container.append(groupHtml);
    }
  },

  /**
   * Formata o nome do grupo muscular
   * @param {string} group - Grupo muscular
   * @returns {string}
   */
  formatMuscleGroup(group) {
    const groups = {
      'trapezius': 'Trapézio',
      'chest': 'Peitoral',
      'back': 'Costas',
      'shoulders': 'Ombros',
      'biceps': 'Bíceps',
      'triceps': 'Tríceps',
      'brachialis': 'Braquial',
      'forearms': 'Antebraços',
      'abs': 'Abdômen',
      'obliques': 'Oblíquos',
      'lombar': 'Lombar',
      'iliopsoas': 'Iliopsoas',
      'glutes': 'Glúteos',
      'quadriceps': 'Quadríceps',
      'hamstrings': 'Posterior',
      'calves': 'Panturrilhas',
      'adductors': 'Adutores',
      'abductors': 'Abdutores',
      'cardio': 'Cardio'
    };
    
    return groups[group] || group;
  },

  /**
   * Abre modal de cadastro de exercício
   */
  openNewExerciseModal() {
    console.log('Abrindo modal de cadastro de exercício');
    
    // Fecha o dropdown do Select2
    $('.select-exercicio').select2('close');
    
    // Abre o modal de cadastro
    const modal = new bootstrap.Modal(document.getElementById('modalCadExercicio'));
    modal.show();
  },

  /**
   * Recarrega o cache de exercícios
   */
  async reloadCache() {
    console.log('Recarregando cache de exercícios...');
    
    // Limpa o cache
    this.cache = null;
    CacheManager.clear();
    
    // Recarrega o cache
    await this.loadExercises();
    console.log('Cache de exercícios recarregado');
    
    // Reinicializa todos os selects
    $('.select-exercicio').each(function() {
      const $this = $(this);
      const currentValue = $this.val();
      
      // Reinicializa o Select2
      ExerciseManager.configureSelect2($this);
      
      // Restaura o valor se havia algum selecionado
      if (currentValue && ExerciseManager.cache) {
        const currentExercise = ExerciseManager.cache.find(e => e.id == currentValue);
        if (currentExercise) {
          const option = new Option(currentExercise.nome, currentExercise.id, true, true);
          $this.append(option).trigger('change');
        }
      }
    });
  }
};

// Exporta para uso global
window.ExerciseManager = ExerciseManager;

