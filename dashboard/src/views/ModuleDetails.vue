<template>
  <div class="container mt-4">
    <h1 class="mb-4">Module: {{ moduleName }}</h1>
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else>
      <h2>Details</h2>
      <p><strong>Name:</strong> {{ moduleName }}</p>
      <p><strong>Description:</strong> {{ module?.description || "No description available" }}</p>
      <p><strong>Routes:</strong> {{ module?.routes_count || 0 }}</p>
      <p><strong>Active:</strong> {{ module?.is_active ? "Yes" : "No" }}</p>
      <router-link to="/" class="btn btn-secondary mt-3">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ModuleDetails",
  props: ["moduleName"],
  computed: {
    ...mapState(["modules", "loading", "error"]),
    module() {
      return this.modules.find((mod) => mod.name === this.moduleName);
    },
  },
};
</script>