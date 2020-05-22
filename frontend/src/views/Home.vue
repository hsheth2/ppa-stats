<template>
  <div class="home">
    <PackageSelection />
  </div>
</template>

<script>
// @ is an alias to /src
import PackageSelection from '@/components/PackageSelection.vue'

export default {
  name: 'Home',
  components: {
    PackageSelection
  }
}
</script>
