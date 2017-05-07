$(document).ready(function() {
	MagnusFlora.initEventHandlers();
});

var MagnusFlora = {
	initEventHandlers: function() {
	},

	formSubmit: function(module, operation, request) {
		var url = '/MagnusFlora/' + module + '/' + operation;

		$.ajax({
			type: "POST",
			contentType: "application/json; charset=utf-8",
			url: url,
			data: request,
			dataType: "json",
			success: MagnusFlora.submitCompleted,
			error: MagnusFlora.submitFailed
		});
	},

	submitCompleted: function(data, status, xhr) {
		if(status == "success") {
			console.log("Submit succeeded. " + JSON.stringify(data.response));
			$("#response").val(JSON.stringify(data.response));
		} else if(status == "error") {
			console.log("Submit failed.");
		}
	},

	submitFailed: function(xhr, ajaxOptions, thrownError) {
		alert("Submit failed: " + xhr.statusText);
	}
};


function sendGenericMessage()
{
	var module = $('#module').val();
	var operation = $('#operation').val();
	var request = $('#request').val();

	console.log("Request: /MagnusFlora/" + module + "/" + operation + ": " + request);
	MagnusFlora.formSubmit(module, operation, request);
	return false;
}

