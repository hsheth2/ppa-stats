<template>
  <div class="main">
    <div class="section main-content">
      <div class="container">
        <h1 class="title">PPA Download Stats</h1>
        <p class="subtitle is-spaced">
          The fastest way to view download statistics for a package published in
          a PPA on Launchpad.
        </p>

        <PackageSelection v-bind.sync="input" @selectPackage="handleSelect" />

        <hr />

        <PackageStats v-bind="selection" />
      </div>
    </div>

    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          <strong>PPA Download Stats</strong> by
          <a href="https://harshal.sheth.io/">Harshal Sheth</a>. View the source
          code on
          <a href="https://github.com/hsheth2/ppa-stats"
            ><b-icon icon="github"></b-icon> Github</a
          >.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
// @ is an alias to /src
import PackageSelection from '@/components/PackageSelection.vue';
import PackageStats from '@/components/PackageStats.vue';

export default {
  name: 'Main',
  components: {
    PackageSelection,
    PackageStats,
  },
  data: () => ({
    input: {
      ppaName: '',
      ppaOwner: '',
      packageName: '',
    },
  }),
  computed: {
    selection() {
      return {
        ppaName: this.$route.query.ppaName || '',
        ppaOwner: this.$route.query.ppaOwner || '',
        packageName: this.$route.query.packageName || '',
      };
    },
  },
  created() {
    Object.assign(this.input, this.selection);
  },
  methods: {
    handleSelect() {
      this.$router.replace({
        name: 'main',
        query: this.input,
      });
    },
  },
};
</script>

<style scoped>
.main {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.main-content {
  flex: 1 0 auto;
}
</style>
