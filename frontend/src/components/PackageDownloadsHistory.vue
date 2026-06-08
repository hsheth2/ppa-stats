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

const FALLBACK_CHART_COLORS = {
  text: '#3f4654',
  mutedText: '#6f7786',
  grid: 'rgba(110, 120, 135, 0.35)',
  line: '#3e8ed0',
  pointBorder: '#ffffff',
};

function readCssVariable(style, name, fallback) {
  return style.getPropertyValue(name).trim() || fallback;
}

function readBulmaHsla(style, hueName, saturationName, lightnessName, alpha) {
  const hue = readCssVariable(style, hueName, '');
  const saturation = readCssVariable(style, saturationName, '');
  const lightness = readCssVariable(style, lightnessName, '');

  if (!hue || !saturation || !lightness) {
    return null;
  }

  return `hsla(${hue}, ${saturation}, ${lightness}, ${alpha})`;
}

function readChartColors() {
  const style = getComputedStyle(document.documentElement);

  return {
    text: readCssVariable(style, '--bulma-text', FALLBACK_CHART_COLORS.text),
    mutedText: readCssVariable(
      style,
      '--bulma-text-weak',
      FALLBACK_CHART_COLORS.mutedText
    ),
    grid:
      readBulmaHsla(
        style,
        '--bulma-scheme-h',
        '--bulma-scheme-s',
        '--bulma-border-weak-l',
        0.85
      ) || FALLBACK_CHART_COLORS.grid,
    line:
      readBulmaHsla(
        style,
        '--bulma-link-h',
        '--bulma-link-s',
        '--bulma-link-on-scheme-l',
        0.9
      ) ||
      readCssVariable(
        style,
        '--bulma-link-on-scheme',
        FALLBACK_CHART_COLORS.line
      ),
    pointBorder: readCssVariable(
      style,
      '--bulma-scheme-main',
      FALLBACK_CHART_COLORS.pointBorder
    ),
  };
}

function downloadsDataset(colors, data) {
  return {
    label: 'Downloads',
    borderColor: colors.line,
    pointBackgroundColor: colors.line,
    pointBorderColor: colors.pointBorder,
    pointHoverBackgroundColor: colors.pointBorder,
    pointHoverBorderColor: colors.line,
    borderWidth: 1.75,
    fill: false,
    pointBorderWidth: 0,
    pointHitRadius: 8,
    pointHoverBorderWidth: 2,
    pointHoverRadius: 4,
    pointRadius: 0,
    tension: 0.15,
    data,
  };
}

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
    chartColors: FALLBACK_CHART_COLORS,
    colorSchemeQuery: null,
    themeChangeHandler: null,
    themeObserver: null,
  }),
  computed: {
    options() {
      const colors = this.chartColors;

      return {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: 'nearest',
        },
        plugins: {
          legend: {
            labels: {
              color: colors.text,
            },
          },
        },
        scales: {
          x: {
            type: 'time',
            time: {
              round: 'day',
              minUnit: 'day',
              tooltipFormat: 'YYYY-MM-DD',
            },
            border: {
              color: colors.grid,
            },
            grid: {
              color: colors.grid,
              tickColor: colors.grid,
            },
            ticks: {
              color: colors.mutedText,
            },
          },
          y: {
            beginAtZero: true,
            border: {
              color: colors.grid,
            },
            grid: {
              color: colors.grid,
              tickColor: colors.grid,
            },
            ticks: {
              color: colors.mutedText,
            },
          },
        },
      };
    },
    chartData() {
      const dates = [];
      const downloads = {};
      const colors = this.chartColors;

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
          datasets: [downloadsDataset(colors, [])],
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
          downloadsDataset(
            colors,
            sortedDownloads.map((entry) => ({
              x: entry[0],
              y: entry[1],
            }))
          ),
        ],
      };
    },
  },
  mounted() {
    this.syncChartColors();
    this.themeChangeHandler = () => this.syncChartColors();

    this.colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    this.colorSchemeQuery.addEventListener('change', this.themeChangeHandler);

    this.themeObserver = new MutationObserver(this.themeChangeHandler);
    this.themeObserver.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class', 'data-theme'],
    });
    this.themeObserver.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme'],
    });
  },
  beforeUnmount() {
    if (this.colorSchemeQuery && this.themeChangeHandler) {
      this.colorSchemeQuery.removeEventListener(
        'change',
        this.themeChangeHandler
      );
    }

    if (this.themeObserver) {
      this.themeObserver.disconnect();
    }
  },
  methods: {
    syncChartColors() {
      this.chartColors = readChartColors();
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
