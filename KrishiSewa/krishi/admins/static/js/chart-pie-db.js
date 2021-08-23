// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

const all_eqp = [ "Tractor", "Harvester", "ATV or UTV", "Plows", "Harrows",
                  "Fertilizer Spreaders", "Seeders", "Balers", "Other",]

const eqp_sales = JSON.parse(document.getElementById('eqp_sales').textContent);
const eqp_labels = [];
const eqp_values = [];

for (var i=0; i<eqp_sales.length; i++) {
  eqp_labels[i] = Object.keys(eqp_sales[i])[0]
  eqp_values[i] = Object.values(eqp_sales[i])[0]
}

while (eqp_values.length < 5) {
  for(var j=0; j<5; j++) {
    if (!linearSearch(all_eqp[j], eqp_labels)) {
      break;
    }
  }
  eqp_labels.push(labels[j])
  eqp_values.push(0)
}
console.log(eqp_labels)

// Pie Chart Example
var ctx = document.getElementById("vendorPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: eqp_labels,
    datasets: [{
      data: eqp_values,
      backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
