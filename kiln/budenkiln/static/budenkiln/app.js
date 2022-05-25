const POINT_COLOR_DEFAULT = "rgba(0,50,200,1)";
const POINT_COLOR_SELECTED = "rgba(200,15,15,1)";

const POINT_RADIUS_DEFAULT = 8;
const POINT_RADIUS_SELECTED = 15;

const MAX_TEMPEARTURE = 1100;

var selectedPoint = null;

const data = {
    datasets: [
        {
            label: 'Temperature Target Curve',
            data: [],
            fill: false,
            pointRadius: POINT_RADIUS_DEFAULT,
            pointHoverRadius: POINT_RADIUS_SELECTED,
            pointBackgroundColor: POINT_COLOR_DEFAULT,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0
        },
        {
            label: 'Temperature History',
            data: [],
            fill: false,
            pointRadius: 1,
            pointHoverRadius: 1,
            pointBackgroundColor: 'rgba(150,0,0,1)',
            borderColor: 'rgb(150, 0, 0)',
            tension: 0
        }
    ]
};

function select(datasetIndex, index) {
    var dataset = data.datasets[datasetIndex];

    var colors = Array(dataset.data.length).fill(POINT_COLOR_DEFAULT);
    var radii = Array(dataset.data.length).fill(POINT_RADIUS_DEFAULT);
    colors[index] = POINT_COLOR_SELECTED;
    radii[index] = POINT_RADIUS_SELECTED;

    dataset.pointRadius = radii;
    dataset.pointBackgroundColor = colors;
    selectedPoint = {
        dataset: datasetIndex,
        index: index,
    };

    for (const elem of document.getElementsByClassName('edit-selected')) {
        elem.disabled = false;
    }

    updatePointText()
}

function deselect() {
    if (selectedPoint != null) {
        var dataset = data.datasets[selectedPoint.dataset];

        // Setting a single value causes an issue with Chart.js where a point is
        // still selected.
        dataset.pointBackgroundColor = Array(dataset.data.length).fill(POINT_COLOR_DEFAULT);
        dataset.pointRadius = Array(dataset.data.length).fill(POINT_RADIUS_DEFAULT);
        selectedPoint = null;

        for (const elem of document.getElementsByClassName('edit-selected')) {
            elem.disabled = true;
        }

        updatePointText();
    }
}

function updatePointText() {
    var textTime = "---";
    var textTemp = "---";

    if (selectedPoint != null) {
        textTime = Math.round(getSelectedPoint().x).toString() + "min";
        textTemp = Math.round(getSelectedPoint().y).toString() + "\u00B0C";
    }

    document.getElementById('selected-time-text').textContent = textTime;
    document.getElementById('selected-temp-text').textContent = textTemp;
}

function getSelectedPoint() {
    return data.datasets[selectedPoint.dataset].data[selectedPoint.index];
}

function sortDataKeepSelected(data, selected) {
    var dataArray = data.datasets[selected.dataset].data;
    var point = dataArray[selected.index];

    dataArray.sort((a, b) => { return a.x - b.x });

    select(selected.dataset, dataArray.findIndex((element) => element == point));
}

chart = new Chart(document.getElementById("myChart"), {
    type: "line",
    data: data,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                suggestedMin: 0,
                suggestedMax: 3600,
                type: 'linear',
                title: {
                    text: "Zeit in Sekunden",
                    display: true,
                },
            },
            y: {
                suggestedMin: 0,
                suggestedMax: 1100,
                ticks: {
                    // Do not allow negative temperature values.     
                    beginAtZero: true,
                },
                title: {
                    text: "Temperatur in C°",
                    display: true,
                },
            },
        },
        animation: {
            duration: 0,
        },
        plugins: {
            title: {
                text: "Härteofen",
                // Disabled so that header can be above button
                display: false,
            },
            legend: {
                display: false,
            }
        },

        onClick: (e, items) => {
            if (items.length == 0) {
                // Get the graph values from the event coordinates.
                const canvasPosition = Chart.helpers.getRelativePosition(e, chart);
                var dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
                var dataY = chart.scales.y.getValueForPixel(canvasPosition.y);

                // Make sure that the time is always positive.
                dataX = Math.max(0, dataX);

                // Make sure that the temperature is positive and does not exceed the temperature range.
                dataY = Math.max(0, Math.min(MAX_TEMPEARTURE, dataY));

                if (selectedPoint == null) {
                    // Create a new data point at x, y. 
                    data.datasets[0].data.push({ x: dataX, y: dataY });
                    data.datasets[0].data.sort((a, b) => { return a.x - b.x });
                } else {
                    // Move the previously selected data point to x, y. 
                    data.datasets[selectedPoint.dataset].data[selectedPoint.index] = { x: dataX, y: dataY };
                    sortDataKeepSelected(data, selectedPoint);
                }

                chart.update();
            } else {
                var item = items[0];

                if (selectedPoint != null &&
                    selectedPoint.dataset == item.datasetIndex &&
                    selectedPoint.index == item.index) {
                    // Deselect the data point if it is currently selected.                                
                    deselect();
                } else {
                    select(item.datasetIndex, item.index);
                }

                chart.update();
            }
        }
    }
});

function onDelete() {
    if (selectedPoint != null) {
        data.datasets[selectedPoint.dataset].data.splice(selectedPoint.index, 1);
        deselect();
        chart.update();
    }
}

function moveTemp(delta) {
    if (selectedPoint != null) {
        var point = getSelectedPoint();

        // Make sure that the temperature is positive and does not exceed the temperature range.
        point.y = Math.max(0, Math.min(MAX_TEMPEARTURE, point.y + delta));
        updatePointText();
        chart.update();
    }
}

function moveTime(delta) {
    if (selectedPoint != null) {
        var point = getSelectedPoint();

        // Make sure that the time is always positive.
        point.x = Math.max(0, point.x + delta);

        sortDataKeepSelected(data, selectedPoint);
        updatePointText();
        chart.update();
    }
}

document.addEventListener('click', function (event) {
    var isClickInsideElement = document.getElementById('chart').contains(event.target);
    if (!isClickInsideElement) {
        deselect();
        chart.update();
    }
});

function display_temperature_history() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `api/history`);
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function() {
        if (xhr.status != 200) {
            alert("Error fetching temperature history");
        } else {
            data.datasets[1].data = xhr.response;
            chart.update();
        }
    }
}

setInterval(display_temperature_history, 1000);

function submit_chart() {
    const curveName = document.getElementById("curve-name").value;
    
    var curve_request_data = {
        name: curveName,
    };
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "api/curve", false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(curve_request_data));
    
    var point_request_data = [];
    data.datasets[0].data.forEach((point) => {
        point_request_data.push({
            time: parseInt(point.x),
            temperature: parseInt(point.y),
        })
    })
    test = JSON.stringify(point_request_data);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", `api/curve/${curveName}/point`, false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    xhr.send(JSON.stringify(point_request_data));
}