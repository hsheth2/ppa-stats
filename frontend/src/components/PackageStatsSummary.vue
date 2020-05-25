<template>
  <nav class="level">
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Total Downloads</p>
        <p class="title">{{ totalDownloads }}</p>
      </div>
    </div>
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Published Binaries</p>
        <p class="title">{{ publishedBinaries }}</p>
      </div>
    </div>
    <div class="level-item has-text-centered">
      <div>
        <p class="heading">Published Versions</p>
        <p class="title">{{ versions }}</p>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'PackageStatsSummary',
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  computed: {
    totalDownloads() {
      return this.data.reduce((total, binary) => {
        return total + binary.total_downloads;
      }, 0);
    },
    publishedBinaries() {
      return this.data.length;
    },
    versions() {
      const versions = new Set();
      for (const binary of this.data) {
        versions.add(binary.version);
      }
      return versions.size;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
