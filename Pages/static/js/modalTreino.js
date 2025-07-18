/**
 * Arquivo principal para o modal de treino
 * Coordena a inicialização e integração de todos os módulos
 */

// Funções globais para compatibilidade com HTML inline
window.mostrarInputNovaSerie = () => UIManager.showNewSeriesInput();
window.adicionarAbaTreino = (name) => WorkoutManager.addWorkoutTab(name);
window.adicionarExercicio = (workoutId) => WorkoutManager.addExercise(workoutId);
window.salvarTreino = () => WorkoutManager.saveWorkout();
window.abrirEdicaoEmMassa = (workoutId) => WorkoutManager.openMassEdit(workoutId);
window.abrirModalCadastroExercicio = () => ExerciseManager.openNewExerciseModal();
window.handleMetodoChange = (selectEl) => WorkoutManager.handleMethodChange(selectEl);

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  UIManager.init();
});

// Compatibilidade com código legado
window.exercisesCache = null;
window.isLoadingExercises = false;

// Funções de compatibilidade
window.carregarExercicios = () => ExerciseManager.loadExercises();
window.filtrarExercicios = (term) => ExerciseManager.filterExercises(term);
window.configurarSelect2Exercicio = ($select) => ExerciseManager.configureSelect2($select);
window.recarregarExercicios = () => ExerciseManager.reloadCache();
window.mostrarNotificacao = (message, type) => UIManager.showNotification(message, type);
window.atualizarGraficoMuscular = (muscleGroup) => BodyGraphManager.updateGraph(muscleGroup);
window.recalcularLinha = (mainRow) => WorkoutManager.recalculateRow(mainRow);

// Atualiza referências globais quando o cache é carregado
ExerciseManager.loadExercises().then(() => {
  window.exercisesCache = ExerciseManager.cache;
});

console.log('Modal de treino carregado e inicializado');

