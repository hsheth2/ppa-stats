<template>
  <div class="home">
    <PackageSelection
      v-bind:ppaName.sync="ppaName"
      v-bind:ppaOwner.sync="ppaOwner"
      v-bind:packageName.sync="packageName"
    />
  </div>
</template>

<script>
// @ is an alias to /src
import PackageSelection from '@/components/PackageSelection.vue'

export default {
  name: 'Home',
  data: () => ({
    ppaName: '',
    ppaOwner: '',
    packageName: ''
  }),
  components: {
    PackageSelection
  }
}
</script>
