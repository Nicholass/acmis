	function viewResults() {
		var div = document.getElementById("poll_results");
		if (div) {
			if (div.style.display == 'none' || div.style.display == '') {
				div.style.display = 'block';
			} else {
				div.style.display = 'none';
			}
		}
		return false;
	}