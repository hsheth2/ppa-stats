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
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  }),
  computed: {
    chartData() {
      const dates = [];
      const downloads = {};
      for (const binary of this.data) {
        for (const [rawDate, count] of Object.entries(binary.daily_downloads)) {
          const date = moment(rawDate, 'YYYY-MM-DD', true);
          dates.push(date);
          if (!(date in downloads)) {
            downloads[date] = 0;
          }
          downloads[date] += count;
        }
      }

      // Fill missing dates in range with 0's.
      const startDate = Math.min(...dates);
      const endDate = Math.max(...dates);
      let date = moment(startDate);
      while (date <= endDate) {
        if (!(date in downloads)) {
          dates.push(date);
          downloads[date] = 0;
        }
        date.add(1, 'days');
      }

      // Sort downloads by date.
      dates.sort((a, b) => a.valueOf() - b.valueOf());
      const sortedDownloads = dates.map((date) => {
        return [date, downloads[date]];
      });

      // Transform into Chart.js format.
      return {
        datasets: [
          {
            label: 'Downloads',
            data: sortedDownloads.map((entry) => ({
              t: entry[0],
              y: entry[1],
            })),
          },
        ],
      };
    },
  },
  watch: {
    chartData: function () {
      this.renderChart(this.chartData, this.options);
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
