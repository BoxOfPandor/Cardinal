<template>
  <div class="container mt-4">
    <h1 class="mb-4">System Health</h1>
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else>
      <h2>Status</h2>
      <p><strong>Status:</strong> {{ health.status }}</p>
      <p><strong>Version:</strong> {{ health.version }}</p>
      <router-link to="/" class="btn btn-secondary mt-3">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "SystemHealth",
  computed: {
    ...mapState(["health", "loading", "error"]),
  },
  created() {
    this.fetchHealth();
  },
  methods: {
    ...mapActions(["fetchHealth"]),
  },
};
</script>