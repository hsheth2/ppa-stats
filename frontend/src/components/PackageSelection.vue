<template>
  <div class="section">
    <div class="container">
      <div class="columns">
        <div class="column">
          <b-field label="PPA Owner">
            <b-input
                v-model="ppaOwner"
                placeholder="PPA owner">
            </b-input>
        </b-field>
        </div>

        <div class="column">
          <b-field label="PPA Name">
            <b-autocomplete
                v-model="ppaName"
                :loading="ppaNameSuggestionsLoading"
                :data="filteredPpaNameSuggestions"
                placeholder="PPA name"
                open-on-focus
                clearable
                @select="option => ppaName = option">
                <template slot="empty">No results found</template>
            </b-autocomplete>
        </b-field>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import debounce from 'lodash/debounce'

export default {
  name: 'PackageSelection',
  data () {
    return {
      ppaOwner: '',
      ppaNameSuggestionsLoading: false,
      ppaNameSuggestions: [],
      ppaName: ''
    }
  },
  computed: {
    filteredPpaNameSuggestions () {
      return this.ppaNameSuggestions.filter((option) => {
        return option
          .toString()
          .toLowerCase()
          .indexOf((this.ppaName || '').toLowerCase()) >= 0
      })
    }
  },
  watch: {
    ppaOwner: debounce(function (ppaOwner) {
      this.ppaNameSuggestionsLoading = true
      this.$http.get(`/api/owner/${ppaOwner}/list_ppas`)
        .then(({ data }) => {
          this.ppaNameSuggestions = []
          console.log(data)
          data.forEach((item) => this.ppaNameSuggestions.push(item))
        })
        .catch((err) => {
          console.log(err)
          this.ppaNameSuggestions = []
        })
        .finally(() => {
          this.ppaNameSuggestionsLoading = false
        })
    }, 500)
  },
  props: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
