var chatArea = document.getElementById('chat-area');
var compose_area = document.getElementById('composer');
var apigClient = apigClientFactory.newClient();
var count = 0;
var botCount = 0;
var userCount = 0;

var nextMessage = {
  message: "",
  sender: ""
};

var order_id;
var user_id;
var cust_number;
var rest_number;
var id_token="12345";
function getTokenID()
{
    var href = window.location.href;
    var parts = href.split('?')[1].split('&');
    order_id = parts[0].split('=')[1];
    cust_number = parts[1].split('=')[1];
    user_id = parts[2].split('=')[1];
    console.log([parts]);
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

function updateInfo(data){
  console.log(data);
  var e = document.createElement('label');
  e.innerHTML = '<label for="name">Customer Name</label><label class="form-control">'+data.customer_name+'</label>';
  var element = document.getElementById("namespace");
  element.appendChild(e);

  e = document.createElement('label');
  e.innerHTML = '<label for="delivery_service">Delivery Service</label><label id="delivery_service" class="form-control validate">'+data.delivery_svc+'</label>';
  element = document.getElementById("delivery_service_space");
  element.appendChild(e);

  e = document.createElement('label');
  e.innerHTML = '<label for="delivery_service">Delivery Address</label><label id="delivery_address" class="long-description validate">'+data.delivery_address+'</label>';
  element = document.getElementById("delivery_address_space");
  element.appendChild(e);

  e = document.createElement('label');
  e.innerHTML = '<label for="delivery_service">Order Cost</label><label class="form-control validate">'+data.order_cost+'</label>';
  element = document.getElementById("order_cost_space");
  element.appendChild(e);  

  e = document.createElement('label');
  e.innerHTML = '<label for="delivery_service">Order Date</label><label class="form-control validate">'+data.order_date+'</label>';
  element = document.getElementById("order_date_space");
  element.appendChild(e);

  e = document.createElement('label');
  e.innerHTML = '<label for="description">Review Description</label><label class="long-description validate tm-small">'+data.order_items+'</label>';
  element = document.getElementById("order_items_space");
  element.appendChild(e);

  rest_number = data.rest_number;
}

function writeMessages(messages){
  var i;
  for(i=0;i<messages.length;i++){
    var m = messages[i];
    console.log(m);
    if(m.user == "user")
      m.user = "bot";
    else
      m.user = 'user';

    sender = m.user;
    t =m.message;
    chatArea.insertAdjacentHTML("beforeend", "<div id='chat-" + count + "' class='chat-container'><div class='chat-wrapper' id='chat-a-" + count + "'><p id='a-' class='chat-" + sender + "'>" + t + "</p><div class='avatar avatar-" + sender + "'></div></div></div>");
  }
}

function displayInitialText() {
  getTokenID();
  params = {
    "order_id": order_id,
    "user_id": user_id,
    "cust_number": cust_number
  }
  apigClient.reviewGet(params, {}, {})
    .then(function(result){
      if (result.data.body == 'Authentication Failure'){
        console.log("Failed Authentication");
        window.location.href = "https://feedme.auth.us-east-1.amazoncognito.com/login?response_type=token&client_id=cjp2ndj6jnj97pb0h6vl62ic6&redirect_uri=https%3A%2F%2Fwww.google.com&fbclid=IwAR2N1UT6LjcMuj0J8QjcHBGOIvGnagES26crsnu2MXCt1NWT4mWofgpMU20";
      }
      console.log(result);
      updateInfo(result.data.body);
      writeMessages(result.data.body.messages);
    }).catch( function(result){
      console.log(result);
      });
}

function sendMessage(){
  sender = "user";
  message = compose_area.value;
  compose_area.value = "";
  body = {
    "cust_number": cust_number,
    "rest_number": rest_number,
    "msg_body": message
  }
  apigClient.reviewPost({}, body, {})
    .then(function(result){
      console.log(result);
    }).catch( function(result){
      console.log(result);
      });
  chatArea.insertAdjacentHTML("beforeend", "<div id='chat-" + count + "' class='chat-container'><div class='chat-wrapper' id='chat-a-" + count + "'><p id='a-' class='chat-" + sender + "'>" + message + "</p><div class='avatar avatar-" + sender + "'></div></div></div>");

}