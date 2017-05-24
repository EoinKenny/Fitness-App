// For Drawing The Google bar Chart
 google.charts.load('current', {'packages':['bar']});


//#--------------------------------------------------------------------------#//
// Execute when page is ready
$(document).ready(function(){
	// Hide these divs on startup
	$("#eoin_page_content").hide();
	$("#form_page_content").hide();
	$("#charts_page_content").hide();
	// More divs in the charts page
	$("#log_workout_form").hide();
	$("#show_chart_form").hide();
	$("#columnchart_material").hide();


	// Slide Toggle the Navigation Bar Options
    $("#eoin_page").click(function(){
		// Toggle main page and hide others
        $("#eoin_page_content").slideToggle(1000);
		// Hide Other pages
		$("#form_page_content").hide(1000);
		$("#charts_page_content").hide(1000);
		$("#log_workout_form").hide(1000);
		$("#show_chart_form").hide(1000);
		$("#columnchart_material").hide(1000);
    });
	
	$("#form_page").click(function(){
		// Toggle form page
        $("#form_page_content").slideToggle(1000);
		// Hide others
		$("#eoin_page_content").hide(1000);
		$("#charts_page_content").hide(1000);
		$("#log_workout_form").hide(1000);
		$("#show_chart_form").hide(1000);
		$("#columnchart_material").hide(1000);
    });
	
	$("#charts_page").click(function(){
		// Toggle charts page
        $("#charts_page_content").slideToggle(1000);
		// Hide Others
		$("#eoin_page_content").hide(1000);
		$("#form_page_content").hide(1000);
		$("#log_workout_form").hide(1000);
		$("#show_chart_form").hide(1000);
		$("#columnchart_material").hide(1000);
    });
	
	// Show Form for submitting workout
	$("#b1").click(function(){
        $("#log_workout_form").slideToggle(1000);
		$("#show_chart_form").hide(1000);
		$("#columnchart_material").hide(1000);

    });
	
	// Show Form for looking at charts 
	$("#b2").click(function(){
        $("#show_chart_form").slideToggle(1000);
		$("#log_workout_form").hide(1000);

    });
	
	
	
	// For Processing the dynamic ajax post request from signUp page
     $('#signUpForm').ajaxForm(function() {
		 
		 // Transfrom data into array of objects
         var data = $("#signUpForm :input").serializeArray();
		 
		 // Check if any values are not filled out
		 if (!data[0].value.length == 0 && !data[1].value.length == 0 && !data[2].value.length == 0) {
			 // Thank user for details or inform them of error
			 var firstName = data[0].value;
			 var lastName = data[1].value;
			 alert("Thank you " + firstName + " " + lastName);
		 } else {
			 alert("You didn't enter all fields correctly.")
		 }
     });

	// For processing the dynamic ajax post request for the 'log a workout' form
	$('#logWorkoutForm').ajaxForm(function() { 
		
		// Transfrom data into array of objects
		var data = $("#logWorkoutForm :input").serializeArray();
		
		 // Check if any values are not filled out
		 if (!data[0].value.length == 0 && !data[1].value.length == 0 && !data[2].value.length == 0 && !data[3].value.length == 0 && !data[4].value.length == 0) {
			 // Thank user for details or inform them of error
			 alert("Thank you, your workout has been logged, keep it up!");
		 } else {
			 alert("You didn't enter all fields correctly.")
		 }
	}); 
	
	// For processing the dynamic ajax get request for the 'get chart' form
	$('#showChartForm').ajaxForm(function() {
		// Get Exercise Type
		var exercise_type = $('input[name="chart_ex_opt"]:checked').val();
		// Toggle the chart div and call the google chart function on callback
		$("#columnchart_material").show(500, function() {
			// Only draw chart if the div is toggeled to 'visible'
			if ($('#columnchart_material').is(":visible")) getWorkoutInfo(exercise_type);
			});
	}); 

});
      

//#--------------------------------------------------------------------------#//
// Calls API for workout info -> Draws Column Charts
function getWorkoutInfo(exercise_type) {
	
	// Get email of client
	var email = document.getElementById('show_chart_email').value;
	
	// API Call -> Get exercise data
	$.getJSON('http://localhost:5000/_get_workouts/' + email, function(info) {
		
		// Draw Google Chart with the exercise information
		drawChart(info, exercise_type);
	});
}


//#--------------------------------------------------------------------------#//
// For Drawing Google Chart
function drawChart(info, exercise_type) {
	
	// Make new google object
	var data = new google.visualization.DataTable();
	
	// Define X axis and bar variables
	data.addColumn('string', 'Date');
	data.addColumn('number', 'Set 1');
	data.addColumn('number', 'Set 2');
	data.addColumn('number', 'Set 3')
	
	// Make empty array for push ups
	var exercise_array = [];
	
	// Make push up array
	for (var i = 0; i < info[exercise_type].length; i++) {
		var date = info[exercise_type][i][0];
		var reps = info[exercise_type][i][1];
	
		// Format the array into something google maps can understand
		reps = reps.split("-").map(Number);
		reps.unshift(date);
		exercise_array.push(reps);
	}
		
	// Add row information
	data.addRows(exercise_array);
	
	// Change formatting of exercise type for display purposes
	switch (exercise_type){
		case "push_ups": exercise_type = "Push Ups"; break;
		case "pull_ups": exercise_type = "Pull Ups"; break;
		case "leg_raises": exercise_type = "Leg Raises"; break;
		case "squats": exercise_type = "Squats"; break;
		default: exercise_type = "Not Defined:"
	}

	var options = {
		chart: {
		title: exercise_type + ' Reps',
		subtitle: 'How Your Gainz Are Progressing ;)',
		}
	};
	// Get div for rendering chart
	var chart = new google.charts.Bar(document.getElementById('columnchart_material'));
	// Draw chart
	chart.draw(data, google.charts.Bar.convertOptions(options));
}