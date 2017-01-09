$(function () {
    Highcharts.chart('pie_people_interested', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            }
        },
        title: {
            text: 'Contents of Highsoft\'s weekly fruit delivery'
        },
        subtitle: {
            text: '3D donut in Highcharts'
        },
        plotOptions: {
            pie: {
                innerSize: 100,
                depth: 45
            }
        },
        series: [{
            name: 'Top 5 Most Favourite Recipes',
            data: [
                ['Recipe 1', 80],
                ['Recipe 2', 70],
                ['Recipe 3', 65],
                ['Recipe 4', 68],
                ['Recipe 5', 70]

            ]
        }]
    });
});


$(function () {
    Highcharts.chart('pie_people_interested', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            }
        },
        title: {
            text: 'Contents of Highsoft\'s weekly fruit delivery'
        },
        subtitle: {
            text: '3D donut in Highcharts'
        },
        plotOptions: {
            pie: {
                innerSize: 100,
                depth: 45
            }
        },
        series: [{
            name: 'Top 5,  5-Rated Recipes',
            data: [
                ['Recipe 1', 80],
                ['Recipe 2', 70],
                ['Recipe 3', 65],
                ['Recipe 4', 68],
                ['Recipe 5', 70]

            ]
        }]
    });
});


$(function () {

  var myChart = Highcharts.chart('chart_nb_interaction', {
      chart: {
          type: 'line'
      },
      title: {
          text: 'Weekly Number of Interaction (Global)'
      },
      xAxis: {
         	categories: ['Mon', 'Tues','Wed', 'Thurs', 'Fri','Sat', 'Sun']

      },
  series: [
        {
          name: 'Favourite',
          data: [7, 6, 9, 14, 18, 21, 25]
        },
        {
          name: 'Comment',
          data: [18, 21, 25, 26, 23, 6, 9]
      }
     ]
  });
});

$(function () {

  var myChart = Highcharts.chart('chart_nb_interaction_spain', {
      chart: {
          type: 'line'
      },
      title: {
          text: 'Weekly Number of Interaction (Spain)'
      },
      xAxis: {
         	categories: ['Mon', 'Tues','Wed', 'Thurs', 'Fri','Sat', 'Sun']

      },
  series: [
        {
          name: 'Favourite',
          data: [7, 6, 9, 14, 18, 21, 25]
        },
        {
          name: 'Comment',
          data: [18, 21, 25, 26, 23, 6, 9]
      }
     ]
  });
});

$(function () {

  var myChart = Highcharts.chart('chart_nb_interaction_France', {
      chart: {
          type: 'line'
      },
      title: {
          text: 'Weekly Number of Interaction (France)'
      },
      xAxis: {
         	categories: ['Mon', 'Tues','Wed', 'Thurs', 'Fri','Sat', 'Sun']

      },
  series: [
        {
          name: 'Favourite',
          data: [7, 6, 9, 14, 18, 21, 25]
        },
        {
          name: 'Comment',
          data: [18, 21, 25, 26, 23, 6, 9]
      }
     ]
  });
});


$(function () {

  var myChart = Highcharts.chart('chart_nb_interaction_germany', {
      chart: {
          type: 'line'
      },
      title: {
          text: 'Weekly Number of Interaction (Germany)'
      },
      xAxis: {
         	categories: ['Mon', 'Tues','Wed', 'Thurs', 'Fri','Sat', 'Sun']

      },
  series: [
        {
          name: 'Favourite',
          data: [7, 6, 9, 14, 18, 21, 25]
        },
        {
          name: 'Comment',
          data: [18, 21, 25, 26, 23, 6, 9]
      }
     ]
  });
});


$(function () {

  var myChart = Highcharts.chart('chart_nb_interaction_belgium', {
      chart: {
          type: 'line'
      },
      title: {
          text: 'Weekly Number of Interaction (Belgium)'
      },
      xAxis: {
         	categories: ['Mon', 'Tues','Wed', 'Thurs', 'Fri','Sat', 'Sun']

      },
  series: [
        {
          name: 'Favourite',
          data: [7, 6, 9, 14, 18, 21, 25]
        },
        {
          name: 'Comment',
          data: [18, 21, 25, 26, 23, 6, 9]
      }
     ]
  });
});
