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
    progress: 0,
    columns: columns,
  }),
  computed: {
    packageSelected() {
      return this.ppaOwner && this.ppaName && this.packageName;
    },
    ppa() {
      return `ppa:${this.ppaOwner}/${this.ppaName}`;
    },
    loading() {
      return this.$asyncComputed.data.updating;
    },
    error() {
      return this.$asyncComputed.data.error;
    },
  },
  asyncComputed: {
    async data() {
      //this.progress = 0;
      if (!this.packageSelected) {
        return Promise.resolve([]);
      }

      const allBinaries = (
        await this.$http.get(
          `/lp-api/1.0/~${this.ppaOwner}/+archive/${this.ppaName}?ws.op=getPublishedBinaries&binary_name=${this.packageName}&exact_match=true`
        )
      ).data.entries;

      // Only fetch downloads for binaries not copied from elsewhere.
      const binaries = allBinaries.filter(
        (entry) => !entry.copied_from_archive_link
      );
      console.log(binaries);

      // testing: change this -- only get first binary
      // return [await this.resolveBinary(binaries[0])];

      const data = await Promise.all(
        binaries.map((entry) => this.resolveBinary(entry))
      );
      return data;
    },
  },
  methods: {
    async resolveBinary(entry) {
      // e.g. self_link: https://api.launchpad.net/1.0/~hsheth2/+archive/ubuntu/ppa/+binarypub/142073665
      const binaryPubId = entry.self_link.split('/').pop();
      const daily_downloads = (
        await this.$http.get(
          `/lp-api/1.0/~${this.ppaOwner}/+archive/ubuntu/${this.ppaName}/+binarypub/${binaryPubId}?ws.op=getDailyDownloadTotals`
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
        package: entry.binary_package_name,
        display_name: entry.display_name,
        status: entry.status,
        build_link: entry.build_link,
        binary_link: entry.self_link,
        version: entry.binary_package_version,
        distro,
        arch,
        total_downloads,
        daily_downloads,
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
