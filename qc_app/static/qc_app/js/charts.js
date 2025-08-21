// 初始化趋势分析图表
function initTrendChart(canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: '质量指标',
                data: [],
                borderColor: '#3e95cd',
                fill: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                annotation: {
                    annotations: []
                }
            },
            scales: {
                x: {title: {display: true, text: '批次/日期'}},
                y: {title: {display: true, text: '测量值'}}
            }
        }
    });
}

// 更新图表数据
function updateTrendChart(chart, data) {
    chart.data.labels = data.labels;
    chart.data.datasets[0].data = data.values;
    
    // 添加标准差线
    const stdLines = [];
    const colors = ['#1cc88a', '#36b9cc', '#f6c23e'];
    
    for (let i = 1; i <= 3; i++) {
        stdLines.push({
            type: 'line',
            yMin: data.mean + i * data.std,
            yMax: data.mean + i * data.std,
            borderColor: colors[i-1],
            borderWidth: 1,
            label: {content: `+${i}σ`}
        });
        // 添加负向标准差线...
    }
    
    chart.options.plugins.annotation.annotations = stdLines;
    chart.update();
}

// 从API获取数据
function fetchChartData(productType, metric) {
    fetch(`/api/chart-data/?type=${productType}&metric=${metric}`)
        .then(response => response.json())
        .then(data => {
            const chart = window.activeChart; // 当前活动图表
            updateTrendChart(chart, data);
        });
}