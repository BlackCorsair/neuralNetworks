$(document).ready(function (){
	$.getJSON('someurl', 'output/output', function(json_data){

    //no need for parsejson
    //use the json_data object

    var table_obj = $('table');
    $.each(json_data, function(index, item){
    	var table_row = $('<tr>', {id: item.id});
    	var table_cell = $('<td>', {html: item.data});
    	table_row.append(table_cell);
    	table_obj.append(table_row);
    })

})
});