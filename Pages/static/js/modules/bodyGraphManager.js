/**
 * Módulo para gerenciamento do gráfico corporal
 * Responsável por carregar e manipular o SVG do corpo humano
 */
const BodyGraphManager = {
  svg: null,
  
  // Cores para os músculos
  COLORS: {
    active: '#00D4FF',
    inactive: '#CBD5E1',
  },

  /**
   * Carrega o gráfico SVG do corpo
   */
  async loadGraph() {
    try {
      const response = await fetch("{% static 'img/body-graph.svg' %}");
      const svgText = await response.text();
      
      // Injeta no DOM
      const wrapper = document.getElementById('modalBodyGraph');
      if (wrapper) {
        wrapper.innerHTML = svgText;
        
        // Guarda referência para manipulação posterior
        this.svg = wrapper.querySelector('svg');
        
        // Inicializa com todos os músculos inativos
        this.colorMuscles([]);
      }
    } catch (error) {
      console.error('Erro ao carregar SVG:', error);
      const placeholder = document.getElementById('body-graph-placeholder');
      if (placeholder) {
        placeholder.innerHTML = 'Erro ao carregar o gráfico corporal.';
      }
    }
  },

  /**
   * Colore músculos específicos
   * @param {Array} activeMuscles - Array de grupos musculares ativos
   */
  colorMuscles(activeMuscles = []) {
    if (!this.svg) return;

    // Normaliza para string (caso venha array de objetos)
    const active = activeMuscles.map(m => 
      typeof m === 'string' ? m : (m.grupo_muscular || m)
    ).filter(Boolean);

    this.svg.querySelectorAll('path[id]').forEach(path => {
      const id = path.id.replace(/\d+$/, ''); // Remove números no final
      const isActive = active.includes(id);
      
      path.style.fill = isActive ? this.COLORS.active : this.COLORS.inactive;
      path.style.cursor = 'pointer';

      // Adiciona evento de clique para alternar o estado
      path.onclick = () => {
        const newState = path.style.fill === this.COLORS.active ? 
          this.COLORS.inactive : this.COLORS.active;
        const baseId = id.replace(/\d+$/, '');
        
        this.svg.querySelectorAll(`path[id^="${baseId}"]`).forEach(p => {
          p.style.fill = newState;
        });
      };
    });
  },

  /**
   * Atualiza o gráfico com todos os músculos dos exercícios
   */
  updateAllMuscles() {
    // Coleta todos os grupos musculares dos exercícios nas abas
    const groups = [];
    
    document.querySelectorAll('.tab-pane[id^="treino_"]').forEach(tabPane => {
      tabPane.querySelectorAll('.exercicio-row').forEach(row => {
        const $selectExercise = $(row).find('.select-exercicio');
        if ($selectExercise.hasClass('select2-hidden-accessible')) {
          const exerciseData = $selectExercise.select2('data')[0];
          if (exerciseData && exerciseData.grupo_muscular) {
            groups.push(exerciseData.grupo_muscular);
          }
        }
      });
    });
    
    this.colorMuscles(groups);
  },

  /**
   * Atualiza o gráfico com um grupo muscular específico
   * @param {string|Array} muscleGroup - Grupo muscular ou array de grupos
   */
  updateGraph(muscleGroup) {
    // Converte para array se for string
    const groups = Array.isArray(muscleGroup) ? muscleGroup : [muscleGroup];
    this.colorMuscles(groups);
  },

  /**
   * Inicializa os event listeners para atualização automática
   */
  initEventListeners() {
    // Atualiza quando exercícios são alterados
    document.addEventListener('input', (e) => {
      if (e.target && e.target.classList.contains('select-exercicio')) {
        setTimeout(() => this.updateAllMuscles(), 100);
      }
    });

    document.addEventListener('change', (e) => {
      if (e.target && e.target.classList.contains('select-exercicio')) {
        setTimeout(() => this.updateAllMuscles(), 100);
      }
    });
  }
};

// Exporta para uso global
window.BodyGraphManager = BodyGraphManager;

