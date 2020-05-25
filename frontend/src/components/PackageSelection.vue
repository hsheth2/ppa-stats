<template>
  <div class="columns">
    <div class="column">
      <b-field label="PPA Owner">
        <b-input
          :value="ppaOwner"
          placeholder="e.g. hsheth2"
          @input="$emit('update:ppaOwner', $event)"
        ></b-input>
      </b-field>
    </div>

    <div class="column">
      <b-field label="PPA Name">
        <b-autocomplete
          :value="ppaName"
          :loading="$asyncComputed.ppaNameSuggestions.updating"
          :data="filteredPpaNameSuggestions"
          placeholder="e.g. apps"
          open-on-focus
          @input="$emit('update:ppaName', $event)"
        >
          <template slot="empty">
            {{ textForSuggestion($asyncComputed.ppaNameSuggestions.state) }}
          </template>
        </b-autocomplete>
      </b-field>
    </div>

    <div class="column">
      <b-field label="Package Name">
        <b-autocomplete
          :value="packageName"
          :loading="$asyncComputed.packageSuggestions.updating"
          :data="filteredPackageSuggestions"
          placeholder="e.g. firefox"
          open-on-focus
          @input="$emit('update:packageName', $event)"
        >
          <template slot="empty">
            {{ textForSuggestion($asyncComputed.packageSuggestions.state) }}
          </template>
        </b-autocomplete>
      </b-field>
    </div>

    <div class="column">
      <b-button class="space-on-top" @click="$emit('selectPackage')"
        >Get Statistics</b-button
      >
    </div>
  </div>
</template>

<script>
const debounce = require('debounce-promise');

export default {
  name: 'PackageSelection',
  props: {
    ppaOwner: { type: String, required: true },
    ppaName: { type: String, required: true },
    packageName: { type: String, required: true },
  },
  computed: {
    filteredPpaNameSuggestions() {
      return (this.ppaNameSuggestions || []).filter((option) => {
        return (
          option.toLowerCase().indexOf((this.ppaName || '').toLowerCase()) >= 0
        );
      });
    },
    filteredPackageSuggestions() {
      return (this.packageSuggestions || []).filter((option) => {
        return (
          option
            .toLowerCase()
            .indexOf((this.packageName || '').toLowerCase()) >= 0
        );
      });
    },
  },
  asyncComputed: {
    ppaNameSuggestions: {
      get: debounce(function () {
        const ppaOwner = this.ppaOwner;
        if (!ppaOwner) {
          return Promise.resolve([]);
        }
        return this.$http
          .get(`/lp-api/1.0/~${ppaOwner}/ppas`)
          .then((response) => {
            const ppas = response.data.entries.map((entry) => entry.name);
            console.log(ppas);
            return ppas;
          });
      }, 500),
      watch: ['ppaOwner'],
    },
    packageSuggestions: {
      get: debounce(function () {
        const ppaOwner = this.ppaOwner;
        const ppaName = this.ppaName;
        if (!ppaOwner || !ppaName) {
          return Promise.resolve([]);
        }
        return this.$http
          .get(
            `/lp-api/1.0/~${ppaOwner}/+archive/${ppaName}?ws.op=getPublishedBinaries`
          )
          .then((response) => {
            const binaries = response.data.entries;
            const packages = new Set(
              binaries.map((binary) => binary.binary_package_name)
            );
            console.log(packages);
            return [...packages];
          });
      }, 500),
      watch: ['ppaOwner', 'ppaName'],
    },
  },
  methods: {
    textForSuggestion(state) {
      if (state === 'updating') {
        return 'Loading suggestions...';
      } else if (state === 'success') {
        return 'No suggestions found.';
      } else {
        return 'Unable to load suggestions.';
      }
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.space-on-top {
  margin-top: 2em;
}
</style>
