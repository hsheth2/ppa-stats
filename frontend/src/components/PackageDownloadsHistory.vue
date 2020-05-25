<script>
import moment from 'moment';
import VueCharts from 'vue-chartjs';

export default {
  name: 'PackageDownloadsHistory',
  extends: VueCharts.Line,
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        xAxes: [
          {
            type: 'time',
            distribution: 'series',
            time: {
              round: 'day',
              minUnit: 'day',
              tooltipFormat: 'YYYY-MM-DD',
            },
          },
        ],
      },
    },
  }),
  computed: {
    chartData() {
      const downloads = {};

      for (const binary of this.data) {
        for (const [rawDate, count] of Object.entries(binary.daily_downloads)) {
          const date = moment(rawDate, 'YYYY-MM-DD', true);
          if (!(date in downloads)) {
            downloads[date] = 0;
          }
          downloads[date] += count;
        }
      }

      // Fill missing dates in range with 0's.
      const dates = Object.keys(downloads);
      const startDate = Math.min(...dates);
      const endDate = Math.max(...dates);
      let date = moment(startDate);
      while (date <= endDate) {
        if (!(date in downloads)) {
          downloads[date] = 0;
        }
        date.add(1, 'days');
      }
      console.log(downloads);

      // Transform into Chart.js format.
      return {
        datasets: [
          {
            label: 'Downloads',
            data: Object.entries(downloads)
              .sort((a, b) => a[0] - b[0])
              .map((entry) => ({
                t: entry[0],
                y: entry[1],
              })),
          },
        ],
      };
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
