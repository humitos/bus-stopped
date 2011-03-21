function loadBusEvent(line){
    if(line == undefined){
        line = line_selected;
    }
    else{
        line_selected = line;
    }
    var direction = $("select[id=direction] option:selected").val();
    var branch_line = $("select[name=branch-line] option:selected").val();
    alert(branch_line);
    // Commented by Issue #28 - https://github.com/humitos/bus-stopped/issues#issue/28
    // var show_path = $("input[id=show-path]").attr('checked', false);
    loadBusStop(line, direction, branch_line);
    showPathEvent();
}

function showPathEvent(){
    var show_path = $("input[id=show-path]").attr("checked");
    hidePaths();
    if(show_path){
        var direction = $("select[id=direction] option:selected").val();
        var branch_line = $("select[name=branch-line] option:selected").val();
        showPath(line_selected, direction, branch_line);
    }
}

function showCardSellPointsEvent(){
    var card_sell_points = $("input[id=show-card-sell-points]").attr("checked");
    if(card_sell_points){
        showCardSellPoints();
    }
    else{
        hideCardSellPoints();
    }
    
}

$(document).ready(function(){
		      $(".line-icon").click(function(event){
						$('.line-icon').addClass('opacity');
						$(this).removeClass('opacity');
						var direction = $("select[id=direction] option:selected").val();
						getBranchLines($(this).attr('id'));
						loadBusEvent($(this).attr('id'));
						return false;
					    });
		      $("select[name='branch-line']").change(function(event){ 
								 loadBusEvent();
							     });
		      $("select[name='direction']").change(function(event){ 
							       loadBusEvent();
							   });
		      now = new Date(CLOCK.year, CLOCK.month, CLOCK.day, CLOCK.hour, CLOCK.minute, CLOCK.second);
		      $(document).ready(function(){var t = setTimeout("clock_tick()", 1000);});
		  });