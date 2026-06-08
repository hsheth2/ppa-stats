<template>
  <div class="chart-container">
    <LineChart :data="chartData" :options="options" />
  </div>
</template>

<script>
import 'chartjs-adapter-moment';
import moment from 'moment';
import {
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  TimeScale,
  Tooltip,
} from 'chart.js';
import { Line as LineChart } from 'vue-chartjs';

ChartJS.register(
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  TimeScale,
  Tooltip
);

export default {
  name: 'PackageDownloadsHistory',
  components: {
    LineChart,
  },
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
        x: {
          type: 'time',
          time: {
            round: 'day',
            minUnit: 'day',
            tooltipFormat: 'YYYY-MM-DD',
          },
        },
        y: {
          beginAtZero: true,
        },
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
          if (!date.isValid()) {
            continue;
          }

          if (!(date in downloads)) {
            dates.push(date);
            downloads[date] = 0;
          }
          downloads[date] += count;
        }
      }

      if (dates.length === 0) {
        return {
          datasets: [
            {
              label: 'Downloads',
              tension: 0.2,
              data: [],
            },
          ],
        };
      }

      // Fill missing dates in range with 0's.
      const startDate = Math.min(...dates);
      const endDate = Math.max(...dates);
      let date = moment(startDate);
      while (date <= endDate) {
        if (!(date in downloads)) {
          dates.push(moment(date));
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
            tension: 0.2,
            data: sortedDownloads.map((entry) => ({
              x: entry[0],
              y: entry[1],
            })),
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
.chart-container {
  min-height: 320px;
  position: relative;
}
</style>
