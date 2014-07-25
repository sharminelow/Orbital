   
			jQuery(document).ready(function() {


				var offset = 220;
				var duration = 500;
				jQuery(window).scroll(function() {
					if (jQuery(this).scrollTop() > offset) {
						jQuery('.back-to-top').fadeIn(duration);
					} else {
						jQuery('.back-to-top').fadeOut(duration);
					}
				});
				
				jQuery('.back-to-top').click(function(event) {
					event.preventDefault();
					jQuery('html, body').animate({scrollTop: 0}, duration);
					return false;
				})


		         $('area').click(function(){
		            $('html, body').animate({
		                scrollTop: $( $(this).attr('href') ).offset().top
		            }, 400);
		            return false;
		        });
   
                
                $('#showmenu').click(function() {
               		$('.menu').slideToggle("fast");
       			});
			
				
				$(".list-group-item").click(function () {
   		 			$(this).toggleClass("clicked");
				});

				$( ".logo" ).hover(function() {
 					 $( this ).fadeOut( 100 );
 					 $( this ).fadeIn( 500 );
				});
 


				/*$('.remove-btn').hover(
					function() {
					$(this).html("<p>Remove</p>");
					},function(){
						var someHtmlString = "<i class = "glyphicon glyphicon-remove"></i>";
                        //var escaped = $("div.someClass").text(someHtmlString).html();
						$(this).text(someHtmlString).html();
					}	
				);*/


				$('#abt-img1').on('mouseover',function() {
					$('#abt-img1').animate({ 'margin-left': -18}), 
					$('#panel1').fadeIn(1000);
					$('#panel1').css({"display": "inline-block", "width":"900px"});		
				});

				$('#abt-img2').on('mouseover',function() {
					$('#abt-img2').animate({ 'margin-left': -18});
					$('#panel2').fadeIn(1000);
					$('#panel2').css({"display": "inline-block", "width":"900px"});				
				});

				$('#abt-img3').on('mouseover',function() {
					$('#abt-img3').animate({ 'margin-left': -18});
					$('#panel3').fadeIn(1000);
					$('#panel3').css({"display": "inline-block", "width":"900px"});
					
				
				});


			});




	

