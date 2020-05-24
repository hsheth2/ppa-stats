<template>
  <div class="section">
    <div class="container">
      <div v-if="loading">
        Loading...
      </div>
      <div v-else-if="packageSelected">
        have some data
        <pre>
          {{ data }}
        </pre>
      </div>
      <div v-else>
        Please select a package.
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';

export default {
  name: 'PackageStats',
  props: {
    ppaOwner: { type: String, required: true },
    ppaName: { type: String, required: true },
    packageName: { type: String, required: true },
  },
  data: () => ({
    loading: false,
    data: [],
  }),
  computed: {
    packageSelected() {
      return this.ppaOwner && this.ppaName && this.packageName;
    },
  },
  watch: {
    ppaOwner: 'fetchData',
    ppaName: 'fetchData',
    packageName: 'fetchData',
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData: debounce(function () {
      if (!this.packageSelected) {
        this.data = [];
        return;
      }
      this.loading = true;
      this.$http
        .get(
          `/api/owner/${this.ppaOwner}/ppa/${this.ppaName}/package/${this.packageName}/downloads`
        )
        .then(({ data }) => {
          this.data = [];
          console.log(data);
          data.forEach((item) => this.data.push(item));
        })
        .catch((err) => {
          console.log(err);
          this.data = [];
        })
        .finally(() => {
          this.loading = false;
        });
    }, 500),
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
