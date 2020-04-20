var rest_token;

function submitForm(){
	var username = document.getElementById("username");
	var password = document.getElementById("password");
	console.log(username.value);
	window.location.href = "index.html?token=" + username.value + "&password="+password.value;
}

document.getElementById("submit_button").addEventListener("click", function(event){
  event.preventDefault();
  submitForm();
});