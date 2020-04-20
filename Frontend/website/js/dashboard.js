Chart.defaults.global.defaultFontColor = 'white';
        let ctxLine,
            ctxBar,
            ctxPie,
            optionsLine,
            optionsBar,
            optionsPie,
            configLine,
            configBar,
            configPie,
            lineChart;
        barChart, pieChart;

var apigClient = apigClientFactory.newClient();
var id_token;
var user_id;

// Extracts tokenID
function getTokenID()
{
    var href = window.location.href;
    
    try{ 
      var parts = href.split('#')[1].split('&');
      id_token = parts[0].split('=')[1];
      var access_id = parts[1].split('=')[1];
      // var expires_in = parts[2].split('=')[1];
      // var token_type = parts[3].split('=')[1];
      return [id_token,access_id]
    }
    catch(error){ 
      return ['lol','you aint in bro']
    }

}
var access_code;
// var at = arr[1];
// var payload = at.split('.')[1]
// var json_string = atob(payload);
function dashboardPage(){
    window.location.href = "index.html#token_id="+id_token+"&user_id="+access_code;
}

function reviewsPage(){
  window.location.href = "products.html?user_id=1";
}
function accountsPage(){
  window.location.href = "accounts.html?user_id="+access_code;
}
window.onload = function() {
  access_code = getTokenID()[1];

  params = {
    "user_id": access_code
  }
  console.log(params);
  apigClient.dashboardGet(params, {}, {})
    .then(function(result){
      console.log(result);
      if (result.data.body == 'Authentication Failure'){
        console.log("Failed Authentication");
        window.location.href = "https://feedme.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=cjp2ndj6jnj97pb0h6vl62ic6&redirect_uri=https%3A%2F%2Fwww.google.com&fbclid=IwAR2N1UT6LjcMuj0J8QjcHBGOIvGnagES26crsnu2MXCt1NWT4mWofgpMU20";
      }
      displaystats(result.data.body);
    }).catch( function(result){
      console.log(result);
      });
}
function showorders(order){
  var e = document.createElement('tr');
  var order_id = order.order_id;
  var name = order.customer_name;
  var delivery_service = order.delivery_service;
  var order_date = order.order_date;
  var restaurant_name = order.restaurant_name;
  e.innerHTML = '<tr><th scope="row"><b>'+order_id+'</b></th><td><b>'+name+'</b></th><td><b>'+delivery_service+'</b></th><td><b>'+order_date+'</b></th><td><b>'+restaurant_name+'</b></th>';
  var element = document.getElementById("orderTable");
  element.appendChild(e);
};


// DOM is ready
function displaystats(data){

  var yelp_data = data.review_perf.Yelp;
  var google_data = data.review_perf.GoogleReviews;
  var opentable_data = data.review_perf.OpenTable;
  var doordash_data = data.rest_perf.Doordash;
  var grubhub_data = data.rest_perf.Grubhub;
  var postmates_data = data.rest_perf.Postmates;
  var seamless_data = data.rest_perf.Seamless;
  var ubereats_data = data.rest_perf.UberEats;
  var i;
  var yelp = [];
  var google = [];
  var opentable = [];

  for(i=0;i<yelp_data.length; i++){
    yelp.push(yelp_data[i][1]);
  }
  for(i=0;i<google_data.length; i++){
    google.push(google_data[i][1]);
  }
  for(i=0;i<opentable_data.length; i++){
    opentable.push(opentable_data[i][1]);
  }

  var doordash = [];
  var grubhub = [];
  var postmates = [];
  var seamless = [];
  var ubereats = [];

  for(i=0;i<doordash_data.length; i++){
    doordash.push(doordash_data[i][1]);
  }
  for(i=0;i<grubhub_data.length; i++){
    grubhub.push(grubhub_data[i][1]);
  }
  for(i=0;i<postmates_data.length; i++){
    postmates.push(postmates_data[i][1]);
  }
  for(i=0;i<seamless_data.length; i++){
    seamless.push(seamless_data[i][1]);
  }
  for(i=0;i<ubereats_data.length; i++){
    ubereats.push(ubereats_data[i][1]);
  }

	ctxLine = document.getElementById("lineChart").getContext("2d");
    optionsLine = {
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Orders"
            }
          }
        ]
      }
    };

    configLine = {
      type: "line",
      data: {
        labels: [
          "July",
          "August",
          "September",
          "October",
          "November", 
          "December"
        ],
        datasets: [
        {
            label: "Google Reviews",
            data: google,
            fill: false,
            borderColor: "rgb(75, 192, 192)",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "Yelp Reviews",
            data: yelp,
            fill: false,
            borderColor: "rgba(255,99,132,1)",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "Open Table",
            data: opentable,
            fill: false,
            borderColor: "rgba(153, 102, 255, 1)",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          }
    
        ]
      },
      options: optionsLine
    };





    ctxBar = document.getElementById("barChart").getContext("2d");
    optionsBar = {
      scales: {
        yAxes: [
          {
            scaleLabel: {
              display: true,
              labelString: "Orders"
            }
          }
        ]
      }
    };

    configBar = {
      type: "line",
      data: {
        labels: [
          "July",
          "August",
          "September",
          "October",
          "November", 
          "December"
        ],
        datasets: [
          {
            label: "Doordash",
            data: doordash,
            fill: false,
            borderColor: "#F7604D",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "GrubHub",
            data: grubhub,
            fill: false,
            borderColor: "#4ED6B8",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "Postmates",
            data: postmates,
            fill: false,
            borderColor: "#A8D582",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "Seamless",
            data: seamless,
            fill: false,
            borderColor: "#D7D768",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          },
          {
            label: "UberEats",
            data: ubereats,
            fill: false,
            borderColor: "#9D66CC",
            cubicInterpolationMode: "monotone",
            pointRadius: 0
          }
        ]
      },
      options: optionsLine
    };



    ctxBar2 = document.getElementById("barChart2").getContext("2d");
    optionsBar2 = {
      responsive: true,
      scales: {
        yAxes: [
          {
            barPercentage: 0.2,
            ticks: {
              beginAtZero: true
            },
            scaleLabel: {
              display: true,
              labelString: "Service"
            }
          }
        ]
      }
    };
    configBar2 = {
      type: "horizontalBar",
      data: {
        labels: ["DoorDash", "GrubHub", "Postmates", "Seamless", "UberEats"],
        datasets: [
          {
            label: "# of Orders",
            data: [doordash.reduce((a, b) => a + b, 0), grubhub.reduce((a, b) => a + b, 0), postmates.reduce((a, b) => a + b, 0), seamless.reduce((a, b) => a + b, 0), ubereats.reduce((a, b) => a + b, 0)],
            backgroundColor: [
              "#F7604D",
              "#4ED6B8",
              "#A8D582",
              "#D7D768",
              "#9D66CC"
              
            ],
            borderWidth: 0
          }
        ]
      },
      options: optionsBar2
    };

    var month_orders = data.month_orders;

    ctxPie = document.getElementById("pieChart").getContext("2d");

    optionsPie = {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 10,
          top: 10,
          bottom: 10
        }
      },
      legend: {
        position: "top"
      }
    };
    configPie = {
      type: "pie",
      data: {
        datasets: [
          {
            data: [
            month_orders.Doordash, 
            month_orders.Grubhub, 
            month_orders.Postmates, 
            month_orders.Seamless, 
            month_orders.UberEats
            ],
            backgroundColor:[
              "#F7604D",
              "#4ED6B8",
              "#A8D582",
              "#D7D768",
              "#9D66CC"
              
            ],
            label: "Monthly Orders"
          }
        ],
        labels: [
          "Doordash",
          "GrubHub",
          "Postmates",
          "Seamless",
          "UberEats"
        ]
      },
      options: optionsPie
    };
	$(function () {
            drawLineChart(); // Line Chart
            drawBarChart(); // Bar Chart
            drawBarChart2() 
            drawPieChart(); // Pie Chart

            $(window).resize(function () {
                updateLineChart();
                updateBarChart();                
            });
        })
  for(i=0;i < data.order_list.length;i++){
        showorders(data.order_list[i]);
      }

}
     


