<template>
  <div class="home">
    <div class="section">
      <div class="container">
        <PackageSelection v-bind.sync="input" @selectPackage="handleSelect" />

        <hr />

        <PackageStats v-bind="selection" />
      </div>
    </div>
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
