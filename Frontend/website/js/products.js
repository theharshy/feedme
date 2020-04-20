var user_id="1";
var apigClient = apigClientFactory.newClient();
var id_token="12345";
function createreviews(review){
	var e = document.createElement('tr');
	var name = review.customer_name;
	var response_state = review.response_state;
	var delivery_service = review.delivery_service;
	var order_date = review.order_date;
	var order_id = review.order_id;
	var customer_number = review.customer_number;
	var restaurant_name = review.restaurant_name;
	e.innerHTML = '<th scope="row"></th><td class="tm-product-name" >'+name+'</td><td>'+response_state+'</td><td>'+delivery_service+'</td><td>'+order_date+'</td><td>'+restaurant_name+'</td>'; 
	e.onclick = function () {
    	window.location.href = "edit-product.html?order_id=" + order_id+'&cust_number='+customer_number+'&user_id='+user_id;
	};
	var element = document.getElementById("tableItems");
	element.appendChild(e);
};
function getTokenID()
{
    var href = window.location.href;
    var parts = href.split('?')[1].split('&');
    user_id = parts[0].split('=')[1];
    console.log(parts);
}

function dashboardPage(){
    window.location.href = "index.html#token_id="+id_token+"&user_id="+user_id;
}

function reviewsPage(){
  window.location.href = "products.html?user_id="+user_id;
}
function accountsPage(){
  window.location.href = "accounts.html?user_id="+user_id;
}

function displayreviews(){
	getTokenID();
	params = {
    "user_id": user_id
  }
  apigClient.reviewsGet(params, {}, {})
    .then(function(result){
      if (result.data.body == 'Authentication Failure'){
        console.log("Failed Authentication");
        window.location.href = "https://feedme.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=cjp2ndj6jnj97pb0h6vl62ic6&redirect_uri=https%3A%2F%2Fwww.google.com&fbclid=IwAR2N1UT6LjcMuj0J8QjcHBGOIvGnagES26crsnu2MXCt1NWT4mWofgpMU20";
      }
      console.log(result);
      reviews = result.data.body.reviews;
      console.log(reviews);
      var i;
      for(i=0;i < reviews.length;i++){
      	createreviews(reviews[i]);
      }
    }).catch( function(result){
      console.log(result);
      });
}

