from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect
from django.conf import settings  # Assuming your Neon CRM credentials are stored in settings
import logging
from ast import literal_eval
from .models import TakenSquare

logger = logging.getLogger('django')
cost_per_square = 20

def square_selection(request):
    if request.method == 'POST':
        # Extract form data
        request.session['form_data'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'selected_squares': request.POST.get('selected_squares'),
        }
        
        return redirect('payment_page')  # Redirect to the payment form
    else:
        grid_size = range(10)  # 10x10 grid
        squares = [[{'taken': False, 'owner': '', 'number': (row, col)}
                    for col in grid_size] for row in grid_size]

        # Load taken squares from the database
        taken_squares = TakenSquare.objects.all()
        for taken_square in taken_squares:
            squares[taken_square.row][taken_square.column]['taken'] = True
            squares[taken_square.row][taken_square.column]['owner'] = f"{taken_square.first_name} {taken_square.last_name}"

        return render(request, 'square_selection.html', {'grid_size': grid_size, 'squares': squares})
    
def payment_page(request):
    if request.method == 'POST':
        # Retrieve form data from session
        form_data = request.session.get('form_data', {})
        card_number = request.POST.get('card_number')
        billing_info = request.POST.get('billing_info')
        
        selected_squares = get_selected_squares(request)
        charge = cost_per_square * len(selected_squares)  # Calculate the charge based on the number of selected squares

        # TODO: Call submit_donation with relevant data
        
        # Save selected squares to database
        if selected_squares:
            for square in selected_squares:
                row, column = square  # Unpack the tuple
                TakenSquare.objects.create(
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name'],
                    email=form_data['email'],
                    row=row,
                    column=column
                )
        
        try:
            del request.session['form_data']
        except KeyError:
            logger.error('Error deleting form_data from session.')

        # Redirect or render a response
        return redirect('success_page')
    else:
        selected_squares = get_selected_squares(request)            
        logger.info("Selected square info", selected_squares, len(selected_squares))
    
        charge = cost_per_square * len(selected_squares)  # Adjust charge calculation as necessary
        return render(request, 'payment_page.html', {'charge': charge})

def submit_donation(cardnumber, address, donor_name, amount):
    # Prepare your payload here. Example:
    payload = {
        "donorName": donor_name,
        "amount": amount,
        # Populate other required fields as per your application's context
    }
    # Prepare the headers with basic authentication
    headers = {
        'Authorization': 'Basic YOUR_ENCODED_CREDENTIALS_HERE',
        'Content-Type': 'application/json',
    }
    # Send the request to Neon CRM API
    response = requests.post('https://api.neoncrm.com/v2/donations', json=payload, headers=headers)


def success_page(request):
    return render(request, 'success_page.html')

def get_selected_squares(request):
    form_data = request.session.get('form_data', {})
    selected_squares_str = form_data.get('selected_squares', '[]')
    try:
        selected_squares = literal_eval(selected_squares_str)
        # Ensure selected_squares is treated as a list
        if isinstance(selected_squares, tuple):
            # Check if the first element of the tuple is also a tuple (indicating multiple selections)
            if isinstance(selected_squares[0], tuple):
                selected_squares = list(selected_squares)  # Convert tuple of tuples to list of tuples
            else:
                selected_squares = [selected_squares]  # Wrap single tuple in a list
    except (ValueError, SyntaxError):
        selected_squares = []  # Handle invalid format
    return selected_squares