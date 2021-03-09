//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	email =document.getElementById('email').value.trim();
	pass1 =document.getElementById('fpass').value.trim();
	cpass=document.getElementById('cpass').value.trim();
	fname=document.getElementById('fname').value.trim();
	lname=document.getElementById('lname').value.trim();
	mobile=document.getElementById('phone').value.trim();
	address=document.getElementById('address').value.trim();
	course=document.getElementById('course').value.trim();
	year=document.getElementById('year').value.trim();
	admno=document.getElementById('admno').value.trim();
	var flag =true;
	if (email==""){
		alert("you are missed to  enter email");
		document.getElementById('sp1').innerHTML="email required";
		flag =false;
	}else {
		const re =/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		if(re.test(String(email).toLowerCase())){
			//do nothing
		}else {
			alert("enter a valid email");
			document.getElementById('sp1').innerHTML="enter valid email";
			flag =false;
		}
	}
	if(pass1==""){
		alert("you are missed to  enter password");
		document.getElementById('sp2').innerHTML="password required";
		flag =false;
	}
	if(cpass==""){
		alert("you are missed to  enter confirm password ");
		document.getElementById('sp3').innerHTML="re-enter password";
		flag =false;
	}
	if(pass1!=cpass){
		alert("passwords are not matched..");
		document.getElementById('sp2').innerHTML="enter the password again";
		document.getElementById('fpass').value="";
		document.getElementById('cpass').value="";
		flag =false;
	}
	if(fname==""){
		alert("you are missed to enter first name");
		document.getElementById('sp4').innerHTML="enter first name";
		flag =false;
	}
	if(lname==""){
		alert("you are missed to enter last name");
		document.getElementById('sp5').innerHTML="enter last name";
		flag =false;
	}
	if(mobile==""){
		alert("you are missed to enter phone number");
		document.getElementById('sp6').innerHTML="enter phone number";
		flag =false;
	}
	if (address==""){
		alert("you are missed to enter address");
		document.getElementById('sp7').innerHTML="enter address";
		flag =false;
	}
	if(course==""){
		alert("you are missed to enter course");
		document.getElementById('sp8').innerHTML="enter course";
		flag =false;
	}
	if(year==""){
		alert("you are missed to enter year");
		document.getElementById('sp9').innerHTML="enter year";
		flag =false;
	}
	if (admno==""){
		alert("you are misssed to enter admission number");
		document.getElementById('sp10').innerHTML="enter admission no.";
		flag =false;
	}
	if(!flag){
		return false;
	}else {
		return true;
	}

})

function clearspan(sp){
	document.getElementById(sp).innerHTML="";

}
