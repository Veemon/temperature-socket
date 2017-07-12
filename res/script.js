// Entry
window.onload = function(){

    // Guage
    var g = new JustGage({
        id: "gauge",
        value: 0,
        min: 0,
        max: 120,
        gaugeWidthScale: 0.5,
        levelColors: ["#a8a8a8", "#ffffff"],
        startAnimationTime: 1000,
        refreshAnimationTime: 3000,
        valueFontColor: "#aaaaaa",
        relativeGaugeSize: true,
      });

    function updateGage(n) {
        g.refresh(n);
    }

    // Chart
    data = [0, 1, 4, 6]
    var ctx = document.getElementById("chart").getContext('2d');
    data = {
      labels: [],
      datasets: [
          {
              label: "Temperature",
              fillColor: "rgba(151,187,205,0.2)",
              strokeColor: "rgba(151,187,205,1)",
              pointColor: "rgba(151,187,205,1)",
              pointStrokeColor: "#fff",
              data: []
          }
      ]
    };
    var chart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            scales: {
                xAxes: [{
                    time: {
                        unit: 'month'
                    }
                }],
                yAxes: [{
                    ticks: {
                        suggestedMin: 40,
                        suggestedMax: 100
                    }
                }]
            }
        }
    });

    function updateChart(label, value){
        chart.data.datasets[0].data.push(value)
        chart.data.labels.push(label)
        chart.update()
    }

    // Socket
    function update(data){
        data = data.split(',');
        updateGage(data[1])
        updateChart(data[0], data[1])
    }

    var ws = new WebSocket("ws://"+window.location.hostname+":80/ws");
    ws.onmessage = function (evt) {
        update(evt.data);
    };
}
