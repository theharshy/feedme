var apigClient = apigClientFactory.newClient();
var title_message = "Thank you, ";
var message_body = "Thank you for ordering ";
var order_id;
var yelp;
var google;
var ot;
function getOrderID()
{
    var href = window.location.href;
    var parts = href.split('?')[1];
    order_id = parts.split('=')[1];
    console.log(order_id);
    // var access_id = parts[1].split('=')[1];
    // var expires_in = parts[2].split('=')[1];
    // var token_type = parts[3].split('=')[1];
    return order_id

}

function yelpReview(){
    console.log("CLICKED!!");
    window.location.href = yelp;
}
function googleReview(){
    window.location.href = google;
}
function opentableReview(){
    window.location.href = ot;
}
function getInfo() {
    order_id = getOrderID();
    params = {
        "order_id": order_id
    }
    apigClient.reviewerGet(params,{},{})
    .then(function(result){
      console.log(result);
      title_message = title_message + result.data.body.customer_name;
      message_body = message_body + result.data.body.order_items+" using "+result.data.body.order_svc+". Please feel free to leave a feedback regarding this order using the buttons below: ";
      document.getElementById("title").innerText = title_message;
      document.getElementById("message").innerText = message_body;
      yelp = result.data.body.yelp_link;
      google = result.data.body.google_link;
      ot = result.data.body.ot_link;
    }).catch( function(result){
      console.log(result);
      });
}