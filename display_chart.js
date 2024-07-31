let DEFAULT_MIN_TEMP = 20
let DEFAULT_MAX_TEMP = 32

// Update title with date of first sample
const date = new Date(data[0]['time'][0]);
const formatter = new Intl.DateTimeFormat('fr-FR', { dateStyle: 'medium' });
const formattedDate = formatter.format(date);
let title = document.getElementById("main_title");
title.innerHTML = 'Fermentation en cours - ' + formattedDate;

let ctx = document.getElementById("myChart").getContext("2d");

// Sample data
let dataset = {
    labels: data[0]['time'],
    datasets: [{
        label: "density",
        data: data[0]['density'],
        backgroundColor: 'rgba(99, 99, 255, 0.2)',
        borderColor: 'rgba(99, 108, 255, 1)',
        borderWidth: 1,
        yAxisID: "y_density",
    },
    {
        label: "temperature",
        data: data[0]['temperature'],
        borderColor: 'rgba(240, 113, 74, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0)',
        borderWidth: 1,
        yAxisID: "y_temp",
        
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
            yAxes: [
                {
                    id: 'y_density',
                    ticks: {
                        min: Math.min(990, Math.floor(Math.min(...data[0]['density'])/10))*10,
                        max: Math.ceil(Math.max(...data[0]['density'])/10)*10
                    },              
                },
                {
                    id: 'y_temp',
                    type: 'linear',
                    display: true,
                    ticks: {
                        min: Math.min(Math.floor(Math.min(...data[0]['temperature']) - 1), DEFAULT_MIN_TEMP), 
                        max: Math.max(Math.max(...data[0]['temperature']) + 1, DEFAULT_MAX_TEMP)
                    },
                    position: 'right',
                }
            ],
        }
    }
});

