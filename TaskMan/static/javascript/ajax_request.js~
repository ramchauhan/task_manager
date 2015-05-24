$(document).ready(function(){
  $('#sort_task').on('click', function(){
	var sort_key = $('#sort_by_kay').find('option:selected').val();
    var all_task = $('.task_wraper').find('.task_lists');
	$.ajax({
	  type: 'GET',
	  url: '/taskman/tasks/sort',
	  data: {sort_key : sort_key },
	  success: function(result) {
		 $(all_task).remove();
		 $.each(result, function(i,item){
	var lists = $('<div class="task_lists" style="width:100%; float:left;"></div>');
    $(lists).append('<span class="task_name" style="width:17%; margin-right:4%;float:left;">'+item.name+'</span>');
    $(lists).append('<span class="task_created_date" style="width:17%; margin-right:4%;float:left;">'+item.created_date+'</span>');
	$(lists).append('<span class="dead_line_date" style="width:17%; margin-right:4%;float:left;">'+item.deat_line_date+'</span>');
	if(item.status == 'INC'){
      $(lists).append('<span class="task_status" style="width:17%; margin-right:3%;float:left;">Not Completed</span>');
	}
	else{
	  $(lists).append('<span class="task_status" style="width:17%; margin-right:3%;float:left;">Completed</span>');
	}   
	$(lists).append('<span class="task_edit" style="width:17%; margin-right:0%;float:left;"><a href="/taskman/delete/'+item.task_id+'">Delete</a></span>')
    $('.task_wraper').append($(lists));
	 });
	 }
	});
  });
});
