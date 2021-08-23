// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById("buyerBarChart");

function linearSearch(value, dataset) {
  for (var index=0; index<dataset.length; index++) {
    if (dataset[index] === value) {
      return true
    }
  }
  return false
}

const product_sales = JSON.parse(document.getElementById('product_sales').textContent);

const prod_labels = [];
const prod_values = [];
for (var i=0; i<product_sales.length; i++) {
  prod_labels[i] = Object.keys(product_sales[i])[0]
  prod_values[i] = Object.values(product_sales[i])[0]
}

while (prod_values.length < 5) {
  // labels from area-char-db.js
  for(var j=0; j<5; j++) {
    if (!linearSearch(labels[j], prod_labels)) {
      break;
    }
  }
  prod_labels.push(labels[j])
  prod_values.push(0)
}

const max_prod_value = Math.max(...prod_values) + 50 

var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: prod_labels,
    datasets: [{
      label: "Revenue",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: prod_values,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: max_prod_value,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
