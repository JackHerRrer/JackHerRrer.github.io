let DEFAULT_MIN_TEMP = 24
let DEFAULT_MAX_TEMP = 30

const under = (ctx, value) => ctx.p0.parsed.y < DEFAULT_MIN_TEMP || ctx.p1.parsed.y < DEFAULT_MIN_TEMP ? value : undefined;
const above = (ctx, value) => ctx.p0.parsed.y > DEFAULT_MAX_TEMP || ctx.p1.parsed.y > DEFAULT_MAX_TEMP ? value : undefined;

// Set default language for date formating
moment.locale('fr');

// Update title with date of first sample
formattedDate = moment(data[0]['time'][0]).format('DD MMM y');
document.getElementById("main_title").innerHTML = 'Fermentation en cours - ' + formattedDate;

let ctx = document.getElementById("myChart").getContext("2d");


// Sample data
let dataset = {
    labels: data[0]['time'],
    datasets: [{
        label: "density",
        data: data[0]['density'],
        backgroundColor: 'rgba(99, 99, 255, 0.05)',
        borderColor: 'rgba(99, 108, 255, 1)',
        borderWidth: 1,
        yAxisID: "y_density",
        pointStyle: false,
        fill : "start",
    },
    {
        label: "temperature",
        data: data[0]['temperature'],
        borderColor: 'rgba(240, 113, 74, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0)',
        borderWidth: 1,
        yAxisID: "y_temp",
        pointStyle: false,
        fill : "shape",
        segment: {
            borderColor: ctx => under(ctx, 'rgb(214, 69, 92)') || above(ctx, 'rgb(214, 69, 92)'),
            backgroundColor: ctx => under(ctx, 'rgb(219, 118, 137,0.2)') || above(ctx, 'rgb(219, 118, 137,0.2)'),
            borderWidth: ctx => under(ctx, 3) || above(ctx, 3),
        },
    }]
};

let chart = new Chart(ctx, {
    type: 'line',
    data: dataset,
    options: {
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                }
            },
            y_density: {
                min: Math.min(990, Math.floor(Math.min(...data[0]['density'])/10))*10,
                max: Math.ceil(Math.max(...data[0]['density'])/10)*10 + 10,
            },
            y_temp :{
                    type: 'linear',
                    display: true,
                    min: Math.min(Math.floor(Math.min(...data[0]['temperature']) - 1), DEFAULT_MIN_TEMP), 
                    max: Math.max(Math.max(...data[0]['temperature']) + 1, DEFAULT_MAX_TEMP),
                    position: 'right',
                    grid: {
                        display : false,
                    }
                }

        }
    }
});

