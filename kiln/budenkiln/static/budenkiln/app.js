const TEMPERATURE_PROFILE_DATASET_LABEL = "Temperature Target Curve"

const POINT_COLOR_DEFAULT = "rgba(0,50,200,1)";
const POINT_COLOR_SELECTED = "rgba(200,15,15,1)";

const POINT_RADIUS_DEFAULT = 8;
const POINT_RADIUS_SELECTED = 15;

const MAX_TEMPEARTURE = 1100;

var selectedPoint = null;

const data = {
    datasets: [
        {
            label: TEMPERATURE_PROFILE_DATASET_LABEL,
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
            pointHitRadius: 0,
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

function getPointInfo(data, index) {
    const point = data[index];
    const newPointText = "".concat(index," : Time ", Math.round(point.x), " - Temp ", Math.round(point.y), "°C");

    return newPointText;
}

function updatePoint(data, index, values) {
    data[index] = values;
    if (selectedPoint != null) {
        sortDataKeepSelected(data, selectedPoint);
    } else {
        data.sort((a, b) => { return a.x - b.x });
    }
    chart.update();

    buildPointList(data);
}

//creates an entry in the point list for each point in data
function buildPointList(data) {
    const listDiv = document.getElementById("list-repr");
    const baseId = "lre-"

    const pointTemplate = document.querySelector("#lre-template");

    //clear existing entries if they exist
    while (listDiv.firstChild) {
        listDiv.removeChild(listDiv.lastChild);
    }

    for (let i = 0; i < data.length; i++) {
        const newPointDiv = pointTemplate.content.cloneNode(true);
        newPointDiv.id = baseId.concat(i);

        const newPointTimeField = newPointDiv.querySelector("#lre-template-time");
        newPointTimeField.id = baseId.concat("time-", i);
        newPointTimeField.value = Math.round(data[i].x)

        const newPointTimeLabel = newPointDiv.querySelector("#lre-template-time-label");
        newPointTimeLabel.id = baseId.concat("time-label-", i);
        newPointTimeLabel.htmlFor = newPointTimeField.id;
        newPointTimeLabel.innerHTML = "Time:"

        const newPointTempField = newPointDiv.querySelector("#lre-template-temp");;
        newPointTempField.id = baseId.concat("temp-", i);
        newPointTempField.value = Math.round(data[i].y);

        const newPointTempLabel = newPointDiv.querySelector("#lre-template-temp-label");
        newPointTempLabel.id = baseId.concat("temp-label-", i);
        newPointTempLabel.htmlFor = newPointTempLabel.id;
        newPointTempLabel.innerHTML = "Temp °C:"

        const newPointDeleteButton = newPointDiv.querySelector("#lre-template-delete-button");
        newPointDeleteButton.id = baseId.concat("del-button-", i);
        newPointDeleteButton.addEventListener('click', function(){
            deletePoint(data, i);
        });

        const newPointApplyButton = newPointDiv.querySelector("#lre-template-apply-button");
        newPointApplyButton.id = baseId.concat("apply-button-", i);
        newPointApplyButton.addEventListener('click', function(){
            const newTime = newPointTimeField.value;
            const newTemp = newPointTempField.value;
            updatePoint(data, i, {x: newTime, y: newTemp});
        });

        listDiv.appendChild(newPointDiv);
    }
}

function insertPoint(data, dataX, dataY) {
    data.push({ x: dataX, y: dataY });
    data.sort((a, b) => { return a.x - b.x });

    buildPointList(data);
}

function deletePoint(data, index) {
    if (selectedPoint != null) {
        deselect();
    }

    data.splice(index, 1);

    buildPointList(data);
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
    var point = data[selected.index];

    data.sort((a, b) => { return a.x - b.x });

    select(selected.dataset, data.findIndex((element) => element == point));
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
                    insertPoint(data.datasets[0].data, dataX, dataY);
                    chart.update();
                } else {
                    // Move the previously selected data point to x, y. 
                    updatePoint(data.datasets[selectedPoint.dataset].data, selectedPoint.index, { x: dataX, y: dataY });
                }
            } else {
                var item = items[0];
                itemDatasetLabel = data.datasets[item.datasetIndex].label
                if (itemDatasetLabel !== TEMPERATURE_PROFILE_DATASET_LABEL) {
                    return;
                }

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
        deletePoint(data.datasets[selectedPoint.dataset].data, selectedPoint.index)
        chart.update();
    }
}

function moveTemp(delta) {
    if (selectedPoint != null) {
        var point = getSelectedPoint();

        // Make sure that the temperature is positive and does not exceed the temperature range.
        point.y = Math.max(0, Math.min(MAX_TEMPEARTURE, point.y + delta));
        updatePoint(data.datasets[selectedPoint.dataset].data, selectedPoint.index, point);
        updatePointText();
        chart.update();
    }
}

function moveTime(delta) {
    if (selectedPoint != null) {
        var point = getSelectedPoint();

        // Make sure that the time is always positive.
        point.x = Math.max(0, point.x + delta)
        updatePoint(data.datasets[selectedPoint.dataset].data, selectedPoint.index, point);
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
    const curveName = "Default";
    
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