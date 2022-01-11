<template>
  <div v-if="loading">
    <h3 class="title is-3">{{ ppa }} - {{ packageName }}</h3>

    <b-message>Loading...</b-message>
    <b-progress
      :value="progress"
      type="is-info"
      size="is-large"
      show-value
      format="percent"
    ></b-progress>
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
import PackageStatsSummary from '@/components/PackageStatsSummary.vue';
import PackageDownloadsHistory from '@/components/PackageDownloadsHistory.vue';

const columns = [
  {
    field: 'binary_package_name',
    label: 'Package',
    sortable: true,
  },
  {
    field: 'binary_package_version',
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
    field: 'status',
    label: 'Status',
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
    columns: columns,
    data: [],
    loading: false,
    error: false,
    progress: 0,
  }),
  computed: {
    packageSelected() {
      return this.ppaOwner && this.ppaName && this.packageName;
    },
    ppa() {
      return `ppa:${this.ppaOwner}/${this.ppaName}`;
    },
    fullSelection() {
      // Exists so that changes to any of the props will trigger a single
      // watch change.
      return `${this.ppa} - ${this.packageName}`;
    },
  },
  watch: {
    fullSelection: 'fetchData',
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      this.loading = true;
      this.error = false;
      this.resolveData()
        .then((data) => {
          this.data = data;
        })
        .catch((err) => {
          console.error(err);
          this.error = true;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async resolveData() {
      this.progress = 0;
      if (!this.packageSelected) {
        return Promise.resolve([]);
      }

      window.umami && window.umami.trackEvent(this.fullSelection.replace('ppa:', ''), 'stats');

      const allBinaries = (
        await this.$http.get(
          `https://api.launchpad.net/1.0/~${this.ppaOwner}/+archive/${this.ppaName}?ws.op=getPublishedBinaries&binary_name=${this.packageName}&exact_match=true&ws.size=300`
        )
      ).data.entries;

      // Deduplication. Each binary is produced by a build, and then optionally copied
      // to a variety of different distribution lists.
      const buildLinks = new Set();
      const binaries = allBinaries.filter((entry) => {
        const buildLink = entry.build_link;
        if (buildLinks.has(buildLink)) {
          return false;
        }
        buildLinks.add(buildLink);
        return true;
      });

      let resolved = 0;
      const data = await Promise.all(
        binaries.map((entry) =>
          this.resolveBinary(entry).finally(() => {
            resolved += 1;
            this.progress = (resolved / binaries.length) * 100;
          })
        )
      );
      console.log(data);
      return data;
    },
    async resolveBinary(entry) {
      // e.g. self_link: https://api.launchpad.net/1.0/~hsheth2/+archive/ubuntu/ppa/+binarypub/142073665
      const binaryPubId = entry.self_link.split('/').pop();
      const daily_downloads = (
        await this.$http.get(
          `https://api.launchpad.net/1.0/~${this.ppaOwner}/+archive/ubuntu/${this.ppaName}/+binarypub/${binaryPubId}?ws.op=getDailyDownloadTotals`
        )
      ).data;
      const total_downloads = Object.values(daily_downloads).reduce(
        (a, b) => a + b,
        0
      );

      // e.g. "cava 0.6.1-0-1 in bionic i386"
      const info = entry.display_name.split(' ');
      const distro = info[3];
      const arch = info[4];

      const binary = {
        distro,
        arch,
        total_downloads,
        daily_downloads,
        ...entry,
      };
      return binary;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.space-bottom {
  margin-bottom: 1.5em;
}
</style>
