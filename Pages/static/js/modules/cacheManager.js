/**
 * Módulo para gerenciamento de cache de exercícios
 * Utiliza sessionStorage para cache temporário com expiração
 */
const CacheManager = {
  CACHE_KEY: 'exercisesCache',
  CACHE_TIMESTAMP_KEY: 'exercisesCacheTimestamp',
  CACHE_DURATION: 30 * 60 * 1000, // 30 minutos

  /**
   * Verifica se o cache é válido
   * @returns {boolean}
   */
  isValid() {
    const timestamp = sessionStorage.getItem(this.CACHE_TIMESTAMP_KEY);
    if (!timestamp) return false;
    
    const now = Date.now();
    const cacheTime = parseInt(timestamp);
    return (now - cacheTime) < this.CACHE_DURATION;
  },

  /**
   * Obtém dados do cache se válidos
   * @returns {Array|null}
   */
  get() {
    if (!this.isValid()) {
      this.clear();
      return null;
    }
    
    const data = sessionStorage.getItem(this.CACHE_KEY);
    return data ? JSON.parse(data) : null;
  },

  /**
   * Armazena dados no cache
   * @param {Array} data - Dados para armazenar
   */
  set(data) {
    sessionStorage.setItem(this.CACHE_KEY, JSON.stringify(data));
    sessionStorage.setItem(this.CACHE_TIMESTAMP_KEY, Date.now().toString());
  },

  /**
   * Limpa o cache
   */
  clear() {
    sessionStorage.removeItem(this.CACHE_KEY);
    sessionStorage.removeItem(this.CACHE_TIMESTAMP_KEY);
  }
};

// Exporta para uso global
window.CacheManager = CacheManager;

