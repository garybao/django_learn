$(document).ready(function() {
	//JQuery code to be added in here.
	$("#about-btn").click(function(event) {
		alert("You clicked the button using JQuery!");
	});
	$(".ouch").click(function(event)) {
		alert("You clicked me! ouch!");
	});
});

$('#likes').click(function(){
	var catid;
	catid = $(this).attr("data-catid");
	$.get('/rango/like_category/', {category_id: catid}, function(data){
		$('#like_count').html(data);
		$('#likes').hide();
	});
});