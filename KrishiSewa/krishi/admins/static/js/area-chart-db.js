// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
const productions = JSON.parse(document.getElementById('productions').textContent);
const labels = ["Cereals", "Pulses", "Vegetables", "Fruits", "Nuts", "Oilseeds",
                "Sugars and Starches", "Fibres", "Beverages", "Narcotics", "Spices", 
                "Condiments", "Others"]
var production_data = [];
for(var i=0; i<labels.length; i++) {
  var key = labels[i]
  production_data[i] = productions[key]
}     
const max_val = Math.max(...production_data) + 100    

var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      label: "Vegetable and Fruits",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: production_data,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'MT'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: max_val,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
