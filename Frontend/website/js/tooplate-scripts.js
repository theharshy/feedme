const width_threshold = 480;

function drawLineChart() {
  if ($("#lineChart").length) {

    // Set aspect ratio based on window width
    optionsLine.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    lineChart = new Chart(ctxLine, configLine);
  }
}

function drawBarChart() {
  if ($("#barChart").length) {

    optionsBar.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    /**
     * COLOR CODES
     * Red: #F7604D
     * Aqua: #4ED6B8
     * Green: #A8D582
     * Yellow: #D7D768
     * Purple: #9D66CC
     * Orange: #DB9C3F
     * Blue: #3889FC
     */

    barChart = new Chart(ctxBar, configBar);
  }
}
function drawBarChart2() {
  if ($("#barChart2").length) {

    optionsBar.maintainAspectRatio =
      $(window).width() < width_threshold ? false : true;

    /**
     * COLOR CODES
     * Red: #F7604D
     * Aqua: #4ED6B8
     * Green: #A8D582
     * Yellow: #D7D768
     * Purple: #9D66CC
     * Orange: #DB9C3F
     * Blue: #3889FC
     */

    barChart2 = new Chart(ctxBar2, configBar2);
  }
}

function drawPieChart() {
  if ($("#pieChart").length) {
    var chartHeight = 300;

    $("#pieChartContainer").css("height", chartHeight + "px");

    pieChart = new Chart(ctxPie, configPie);
  }
}

function updateLineChart() {
  if (lineChart) {
    lineChart.options = optionsLine;
    lineChart.update();
  }
}

function updateBarChart() {
  if (barChart) {
    barChart.options = optionsBar;
    barChart.update();
  }
}
