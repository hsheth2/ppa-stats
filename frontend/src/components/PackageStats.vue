<template>
  <div v-if="loading">
    <b-message>Loading...</b-message>
  </div>
  <div v-else-if="error">
    <b-message type="is-danger">
      Failed to load download statistics for {{ packageName }} in {{ ppa }}. Try
      reloading the page.
    </b-message>
  </div>
  <div v-else-if="packageSelected">
    <h3 class="title is-3">{{ ppa }} - {{ packageName }}</h3>

    <PackageStatsSummary :data="data" />

    <h4 class="is-size-4">Daily Downloads</h4>
    <div class="space-bottom">
      <PackageDownloadsHistory :data="data" />
    </div>

    <h4 class="is-size-4">Detailed Downloads History</h4>
    <b-table :data="data" :columns="columns" :striped="true" />
  </div>
  <div v-else>
    <b-message>Please select a package.</b-message>
  </div>
</template>

<script>
import debounce from 'lodash/debounce';
import PackageStatsSummary from '@/components/PackageStatsSummary.vue';
import PackageDownloadsHistory from '@/components/PackageDownloadsHistory.vue';

const columns = [
  {
    field: 'package',
    label: 'Package',
    sortable: true,
  },
  {
    field: 'version',
    label: 'Version',
    sortable: true,
  },
  {
    field: 'distro',
    label: 'Distribution',
    sortable: true,
  },
  {
    field: 'arch',
    label: 'Architecture',
    sortable: true,
  },
  {
    field: 'total_downloads',
    label: 'Total Downloads',
    sortable: true,
    numeric: true,
  },
];

export default {
  name: 'PackageStats',
  components: {
    PackageStatsSummary,
    PackageDownloadsHistory,
  },
  props: {
    ppaOwner: { type: String, required: true },
    ppaName: { type: String, required: true },
    packageName: { type: String, required: true },
  },
  data: () => ({
    loading: false,
    error: false,
    data: [],
    columns: columns,
  }),
  computed: {
    packageSelected() {
      return this.ppaOwner && this.ppaName && this.packageName;
    },
    ppa() {
      return `ppa:${this.ppaOwner}/${this.ppaName}`;
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
    fetchData: debounce(
      function () {
        if (!this.packageSelected) {
          this.data = [];
          this.error = false;
          return;
        }
        this.loading = true;
        this.$http
          .get(
            `/api/owner/${this.ppaOwner}/ppa/${this.ppaName}/package/${this.packageName}/downloads`
          )
          .then(({ data }) => {
            this.data = data;
            this.error = false;
            console.log(data);
          })
          .catch((err) => {
            console.log(err);
            this.data = [];
            this.error = true;
          })
          .finally(() => {
            this.loading = false;
          });
      },
      500,
      {
        leading: true,
        trailing: true,
      }
    ),
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.space-bottom {
  margin-bottom: 1.5em;
}
</style>
