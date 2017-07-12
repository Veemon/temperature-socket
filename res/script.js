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
      labels: ['0', '1', '2', '3',
                '4', '5', '6'],
      datasets: [
          {
              label: "Temperature",
              fillColor: "rgba(151,187,205,0.2)",
              strokeColor: "rgba(151,187,205,1)",
              pointColor: "rgba(151,187,205,1)",
              pointStrokeColor: "#fff",
              data: [28, 48, 40, 19, 86, 27, 90]
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
                }]
            }
        }
    });

    // Socket
    function update(data){
        console.log(data)
    }

    function open_socket(){
        var ws = new WebSocket("ws://localhost:80/ws");
        ws.onopen = function() {
           ws.send("Hello, world");
        };
        ws.onmessage = function (evt) {
            update(evt.data);
        };
    }

    open_socket();
}
