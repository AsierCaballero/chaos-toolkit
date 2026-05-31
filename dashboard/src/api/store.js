import { defineStore } from "pinia";
import { fetchExperiments } from "./index";

export const useChaosStore = defineStore("chaos", {
  state: () => ({
    experiments: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchExperiments() {
      this.loading = true;
      this.error = null;
      try {
        this.experiments = await fetchExperiments();
      } catch (e) {
        this.error = e.message;
        this.experiments = [];
      } finally {
        this.loading = false;
      }
    },
  },
});
