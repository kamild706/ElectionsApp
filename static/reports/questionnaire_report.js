function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

const ctx = document.getElementById("myChart").getContext('2d');
// Chart.defaults.global.animation.duration = 0;

myLabels = [];
myData = [];
myBackgroundColor = [];
$('.results tbody tr').each(function() {
    myLabels.push(this.cells[1].innerHTML);
    myData.push(Number(this.cells[3].innerHTML.replace(',', '.').replace('%', '')));
    myBackgroundColor.push(getRandomColor());
});

data = {
    datasets: [{
        data: myData,
        backgroundColor: myBackgroundColor,
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: myLabels,
};


const myPieChart = new Chart(ctx, {
    type: 'pie',
    data: data,
});
