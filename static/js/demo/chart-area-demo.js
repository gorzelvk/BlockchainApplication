var months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec"
];

Date.prototype.getMonthName = function() {
  return months[this.getMonth()];
};

function getNextMonth(currentMonth) {
  if (currentMonth == "Dec") {
    return "Jan";
  } else {
    return months[months.indexOf(currentMonth) + 1];
  }
}

function getMonthsToDisplay() {
  var d = new Date();
  var thisMonth = new Date().getMonthName();
  var monthsDisplay = [];
  for (var i = 1; i <= 12; i++) {
    var thisMonth = getNextMonth(thisMonth);
    monthsDisplay.push(thisMonth);
  }

  for (var i = 11; i >= 0; i--) {
    var currentData = monthsDisplay[i];

    if (
      typeof yearAdd == "undefined" ||
      yearAdd == d.getFullYear().toString()
    ) {
      if (i < 11 && monthsDisplay[i] == "Dec") {
        var yearAdd = (d.getFullYear() - 1).toString();
      } else {
        var yearAdd = d.getFullYear().toString();
      }
    }

    monthsDisplay[i] = currentData + " " + yearAdd;
  }

  return monthsDisplay;
}

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";
function myFunc(vars) {
    return vars
}
// Area Chart Example

new Chart("myChart", {
  type: "line",
  data: {
    labels: [0, 1, 2, 3 , 4],
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: [6, 8, 3, 6, 20]
    }]
  },
  options: {
    legend: {display: false},
    scales: {
      yAxes: [{ticks: {min: 6, max:16}}],
    }
  }
});