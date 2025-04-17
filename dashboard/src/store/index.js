import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    modules: [],
    health: {},
    loading: false,
    error: null
  },
  mutations: {
    setModules(state, modules) {
      state.modules = modules
    },
    setHealth(state, health) {
      state.health = health
    },
    setLoading(state, loading) {
      state.loading = loading
    },
    setError(state, error) {
      state.error = error
    }
  },
  actions: {
    async fetchModules({ commit }) {
      commit('setLoading', true)
      try {
        const response = await axios.get('/api/modules')
        commit('setModules', response.data.modules)
        commit('setError', null)
      } catch (error) {
        commit('setError', 'Failed to fetch modules')
        console.error('Error fetching modules:', error)
      } finally {
        commit('setLoading', false)
      }
    },
    async fetchHealth({ commit }) {
      commit('setLoading', true)
      try {
        const response = await axios.get('/api/health')
        commit('setHealth', response.data)
        commit('setError', null)
      } catch (error) {
        commit('setError', 'Failed to fetch system health')
        console.error('Error fetching health:', error)
      } finally {
        commit('setLoading', false)
      }
    }
  }
})