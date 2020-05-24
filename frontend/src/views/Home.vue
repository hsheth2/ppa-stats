<template>
  <div class="home">
    <div class="section">
      <div class="container">
        <PackageSelection
          :ppa-name.sync="ppaName"
          :ppa-owner.sync="ppaOwner"
          :package-name.sync="packageName"
        />

        <hr />

        <PackageStats
          :ppa-name="ppaName"
          :ppa-owner="ppaOwner"
          :package-name="packageName"
        />
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
    ppaName: '',
    ppaOwner: '',
    packageName: '',
  }),
};
</script>
