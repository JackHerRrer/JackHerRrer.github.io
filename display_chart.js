let ctx = document.getElementById("myChart").getContext("2d");

// Sample data
let dataset = {
    labels: data[0]['time'],
    datasets: [{
        label: "density",
        data: data[0]['density'],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(245, 108, 10, 1)',
        borderWidth: 1,
    }]
};

let chart = new Chart(ctx, {
    type: 'line',
    data: dataset,
    options: {

        scales: {
            xAxes: [{
                type: 'time',
                grid:{
                    color: 'yellow'
                },
                time: {
                    unit: 'day',
                    displayFormats: {
                      'millisecond': 'DD MMM HH:mm',
                      'second': 'DD MMM HH:mm',
                      'minute': 'DD MMM HH:mm',
                      'hour': 'DD MMM HH:mm',
                      'day': 'DD MMM',
                      'week': 'DD MMM HH:mm',
                      'month': 'DD MMM HH:mm',
                      'quarter': 'DD MMM HH:mm',
                      'year': 'DD MMM HH:mm',
                    }
                }
            }],
            yAxes: [{
                ticks: {
                    min: 990, 
                    max: Math.ceil(Math.max(...data[0]['density'])/10)*10
                }
            }],
        }
    }
});

