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
  name: 'Home',
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
    selection: {
      ppaName: '',
      ppaOwner: '',
      packageName: '',
    },
  }),
  methods: {
    handleSelect() {
      this.selection = this.input;
    },
  },
};
</script>
