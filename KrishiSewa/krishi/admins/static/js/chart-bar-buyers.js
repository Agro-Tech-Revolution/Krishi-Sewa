// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const prod_data = JSON.parse(document.getElementById('prod_data').textContent);
const all_prod_labels = ["Cereals", "Pulses", "Vegetables", "Fruits", "Nuts", "Oilseeds",
                          "Sugars and Starches", "Fibres", "Beverages", "Narcotics", "Spices",
                          "Condiments", "Others"];

var prod_purchase = [];
for(var i=0; i<all_prod_labels.length; i++) {
  var key = all_prod_labels[i]
  prod_purchase[i] = prod_data[key]
}     
const max_val = Math.max(...prod_purchase) + 100                         



var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: all_prod_labels,
    datasets: [{
      label: "Purchases",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: prod_purchase,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: true
        },
        ticks: {
          maxTicksLimit: 20
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: max_val,
          maxTicksLimit: 20
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: true
    }
  }
});
