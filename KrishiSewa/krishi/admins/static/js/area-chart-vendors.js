// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const sales_data = JSON.parse(document.getElementById('sales_data').textContent);
const all_eqp = [ "Tractor", "Harvester", "ATV or UTV", "Plows", "Harrows",
                  "Fertilizer Spreaders", "Seeders", "Balers", "Other",];

var eqp_sales = [];
for(var i=0; i<all_eqp.length; i++) {
  var key = all_eqp[i]
  eqp_sales[i] = sales_data[key]
}     
const max_val = Math.max(...eqp_sales) + 100                   
                  

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    // labels: ["Tractors", "Kodalo", "Pipes", "Cutter", "Rice-Harvesters", "Loader"],
    labels: all_eqp,
    datasets: [{
      label: "Sells",
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
      data: eqp_sales,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'Thousand'
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
      display: true
    }
  }
});
