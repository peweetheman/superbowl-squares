function selectSquare(element, squareId) {
	// Add selection class to clicked square
	if (element.classList.contains('taken')) { // square is unavailable
		pass;
	}
	if (element.classList.contains('selected')) { // square is selected, unselect it
		element.classList.remove('selected');
		element.classList.add('available');
	}
	else { // square is available, select it
		element.classList.add('selected');
		element.classList.remove('available');
	}

	// Update hidden input value
	document.getElementById('selected_square').value = squareId;
}
