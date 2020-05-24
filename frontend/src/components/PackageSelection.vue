<template>
  <div class="section">
    <div class="container">
      <div class="columns">
        <div class="column">
          <b-field label="PPA Owner">
            <b-input
              :value="ppaOwner"
              placeholder="PPA owner"
              @input="$emit('update:ppaOwner', $event)"
            >
            </b-input>
          </b-field>
        </div>

        <div class="column">
          <b-field label="PPA Name">
            <b-autocomplete
              :value="ppaName"
              :loading="ppaNameSuggestionsLoading"
              :data="filteredPpaNameSuggestions"
              placeholder="PPA name"
              open-on-focus
              @input="$emit('update:ppaName', $event)"
            >
              <template v-if="ppaNameSuggestionsLoading" slot="empty"
                >Loading suggestions...</template
              >
              <template v-else slot="empty">No suggestions found</template>
            </b-autocomplete>
          </b-field>
        </div>

        <div class="column">
          <b-field label="Package Name">
            <b-autocomplete
              :value="packageName"
              :loading="packageSuggestionsLoading"
              :data="filteredPackageSuggestions"
              placeholder="Package name"
              open-on-focus
              @input="$emit('update:packageName', $event)"
            >
              <template v-if="packageSuggestionsLoading" slot="empty"
                >Loading suggestions...</template
              >
              <template v-else slot="empty">No suggestions found</template>
            </b-autocomplete>
          </b-field>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';

export default {
  name: 'PackageSelection',
  props: {
    ppaOwner: { type: String, required: true },
    ppaName: { type: String, required: true },
    packageName: { type: String, required: true },
  },
  data() {
    return {
      ppaNameSuggestionsLoading: false,
      ppaNameSuggestions: [],
      packageSuggestionsLoading: false,
      packageSuggestions: [],
    };
  },
  computed: {
    filteredPpaNameSuggestions() {
      return this.ppaNameSuggestions.filter((option) => {
        return (
          option.toLowerCase().indexOf((this.ppaName || '').toLowerCase()) >= 0
        );
      });
    },
    filteredPackageSuggestions() {
      return this.packageSuggestions.filter((option) => {
        return (
          option
            .toLowerCase()
            .indexOf((this.packageName || '').toLowerCase()) >= 0
        );
      });
    },
  },
  watch: {
    ppaOwner: 'updatePpaNameSuggestions',
    ppaName: 'updatePackageNameSuggestions',
  },
  created() {
    this.updatePpaNameSuggestions();
    this.updatePackageNameSuggestions();
  },
  methods: {
    updatePpaNameSuggestions: debounce(function (ppaOwner) {
      if (!ppaOwner) {
        this.ppaNameSuggestions = [];
        return;
      }
      this.ppaNameSuggestionsLoading = true;
      this.$http
        .get(`/api/owner/${ppaOwner}/list_ppas`)
        .then(({ data }) => {
          this.ppaNameSuggestions = [];
          console.log(data);
          data.forEach((item) => this.ppaNameSuggestions.push(item));
        })
        .catch((err) => {
          console.log(err);
          this.ppaNameSuggestions = [];
        })
        .finally(() => {
          this.ppaNameSuggestionsLoading = false;
        });
    }, 500),
    updatePackageNameSuggestions: debounce(function (ppaName) {
      if (!ppaName) {
        this.packageSuggestions = [];
        return;
      }
      this.packageSuggestionsLoading = true;
      this.$http
        .get(`/api/owner/${this.ppaOwner}/ppa/${ppaName}/list_packages`)
        .then(({ data }) => {
          this.packageSuggestions = [];
          console.log(data);
          data.forEach((item) => this.packageSuggestions.push(item));
        })
        .catch((err) => {
          console.log(err);
          this.packageSuggestions = [];
        })
        .finally(() => {
          this.packageSuggestionsLoading = false;
        });
    }, 500),
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
