<template>
  <div class="home">
    <PackageSelection
      :ppa-name.sync="ppaName"
      :ppa-owner.sync="ppaOwner"
      :package-name.sync="packageName"
    />

    <PackageStats
      :ppa-name="ppaName"
      :ppa-owner="ppaOwner"
      :package-name="packageName"
    />
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
    ppaName: '',
    ppaOwner: '',
    packageName: '',
  }),
};
</script>
