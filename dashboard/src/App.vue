<!-- Cardinal/dashboard/src/views/Dashboard.vue -->
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Cardinal Dashboard</h1>
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else>
      <h2>Modules</h2>
      <div v-if="modules.length === 0" class="alert alert-warning">
        No modules found.
      </div>
      <div class="row">
        <div
          v-for="module in modules"
          :key="module.name"
          class="col-md-4 mb-3"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ module.name }}</h5>
              <p class="card-text">{{ module.description }}</p>
              <p class="card-text">
                <small class="text-muted">Routes: {{ module.routes_count }}</small>
              </p>
              <router-link
                :to="{ name: 'ModuleDetails', params: { moduleName: module.name } }"
                class="btn btn-primary"
              >
                View Details
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "Dashboard",
  computed: {
    ...mapState(["modules", "loading", "error"]),
  },
  created() {
    this.fetchModules();
  },
  methods: {
    ...mapActions(["fetchModules"]),
  },
};
</script>