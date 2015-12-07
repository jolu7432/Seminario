function renderDash(data, DOMElement, TipoGrafico) {
    switch (TipoGrafico) {
        case "barra":
            $(DOMElement).highcharts({
                chart: {
                    type: 'column',
                },
                title: {
                    text: 'Alertas'
                },
                subtitle: {
                    text: "Grafico"
                },
                xAxis: {
                    title: {
                        text: 'Fecha'
                    },
                    categories: data.categories
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Temperatura y Humedad'
                    },
                    stackLabels: {
                        enabled: true,
                        style: {
                            fontWeight: 'bold',
                            color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                        }
                    }
                },
                legend: {
                    align: 'left',
                    verticalAlign: 'bottom',
                    floating: false,
                    backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                    borderColor: '#CCC',
                    borderWidth: 1,
                    shadow: true,
                    maxHeight: 80
                },
                tooltip: {
                    headerFormat: '<span style="font-size:11px"></span>',
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br />',// ({point.percentage:.0f}%)<br/>',
                    shared: true
                },
                plotOptions: {
                    column: {
                        stacking: 'normal'
                    }
                },
                series: data.series
            });

            break;
        case "columna":
            $(DOMElement).highcharts({
                chart: {
                    type: 'column',
                },
                title: {
                    text: 'Alertas'
                },
                subtitle: {
                    text: ' '
                },
                xAxis: {
                    categories: data.categories
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Temperatura y Humedad'
                    },
                    stackLabels: {
                        enabled: true,
                        style: {
                            fontWeight: 'bold',
                            color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                        }
                    }
                },
                legend: {
                    align: 'left',
                    verticalAlign: 'bottom',
                    floating: false,
                    backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                    borderColor: '#CCC',
                    borderWidth: 1,
                    shadow: true,
                    maxHeight: 80
                },
                tooltip: {
                    headerFormat: '<span style="font-size:11px"></span>',
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br />',// ({point.percentage:.0f}%)<br/>',
                    shared: true
                },
                plotOptions: {
                    series: {
                        borderWidth: 0,
                        dataLabels: {
                            enabled: true,
                            format: '{point.y:.0f}'
                        }
                    }
                },
                series: data.series


            });

            break;
        case "torta":
            Highcharts.setOptions({
                lang: {
                    drillUpText: '<< volver'
                }
            });
            $(DOMElement).highcharts({
                chart: {
                    type: 'pie'
                },
                title: {
                    text: 'Alertas'
                },
                subtitle: {
                    text: ' '
                },
                plotOptions: {
                    series: {
                        dataLabels: {
                            enabled: true,
                            format: '{point.name}: {point.y:0.0f}'
                        },
                        showInLegend: true
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:11px"></span>',
                    pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.0f}</b> cant.<br/>'
                },
                series: data.series
            });

            break;
        case "linea":
            $(DOMElement).highcharts({
                chart: {
                    type: 'spline',
                },
                title: {
                    text: 'Alertas'
                },
                subtitle: {
                    text: 'Linea'
                },
                xAxis: {
                    title: {
                        text: 'Fecha'
                    },
                    categories: data.categories
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Temperatura y Humedad'
                    },
                    stackLabels: {
                        enabled: true,
                        style: {
                            fontWeight: 'bold',
                            color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                        }
                    }
                },
                legend: {
                    align: 'left',
                    verticalAlign: 'bottom',
                    floating: false,
                    backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
                    borderColor: '#CCC',
                    borderWidth: 1,
                    shadow: true,
                    maxHeight: 80
                },
                tooltip: {
                    headerFormat: '<span style="font-size:11px"></span>',
                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br />',// ({point.percentage:.0f}%)<br/>',
                    shared: true
                },
                plotOptions: {
                    column: {
                        stacking: 'normal'
                    }
                },
                series: data.series
            });

            break;
        default:
            alert('Gráfico no implementado.');
            break;
    }
};
          