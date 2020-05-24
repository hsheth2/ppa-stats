<template>
  <div class="home">
    <PackageSelection
      :ppa-name.sync="ppaName"
      :ppa-owner.sync="ppaOwner"
      :package-name.sync="packageName"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import PackageSelection from '@/components/PackageSelection.vue';

export default {
  name: 'Home',
  components: {
    PackageSelection,
  },
  data: () => ({
    ppaName: '',
    ppaOwner: '',
    packageName: '',
  }),
};
</script>
