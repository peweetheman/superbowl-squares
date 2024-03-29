from django.http import HttpResponse
from django.shortcuts import render, redirect
import logging
from datetime import datetime
from ast import literal_eval
from .models import TakenSquare
from .neon_api import create_donation
from card_identifier.cardutils import format_card, validate_card
from card_identifier.card_type import identify_card_type
logger = logging.getLogger('django')
cost_per_square = 20

def square_selection(request):
    if request.method == 'POST':
        # Extract form data
        request.session['form_data'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'display_name': request.POST.get('display_name'),
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
            if taken_square.display_name is not None and taken_square.display_name != "":
                squares[taken_square.row][taken_square.column]['owner'] = f"{taken_square.display_name}"
            else: 
                squares[taken_square.row][taken_square.column]['owner'] = f"{taken_square.first_name} {taken_square.last_name}"

        return render(request, 'square_selection.html', {'grid_size': grid_size, 'squares': squares})
    
def payment_page(request):
    selected_squares = get_selected_squares(request)
    num_squares = len(selected_squares)
    charge = cost_per_square * num_squares  # Calculate the charge based on the number of selected squares
    current_year = datetime.now().year
    context = {
        'months': range(1, 13),
        'years': range(current_year, current_year + 10),
        'charge': f"${charge:.2f}",
        'cost_per_square': f"(${cost_per_square} per square)",
        'retry_payment': False, 
    }

    if request.method == 'POST':
        # Retrieve form data from session
        form_data = request.session.get('form_data', {})
        card_number = request.POST.get('cardnumber').replace(' ', '')
        expiration_date = request.POST.get('expirationdate')
        cvv2 = request.POST.get('securitycode')
        card_holder = request.POST.get('cardholder')
        
        # Get the card type and validate
        try:
            card_number = format_card(card_number)
            if not validate_card(card_number):
                raise Exception("Invalid card")
            card_type = identify_card_type(card_number)
        except Exception as e:
            print(e)
            context['retry_payment'] = True
            return render(request, 'payment_page.html', context)


        # submit donation with relevant data
        # donation_succeeded = True
        donation_succeeded = create_donation(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            email=form_data['email'],
            amount=charge,
            card_number=card_number,
            expiration_month=expiration_date.split('/')[0],
            expiration_year="20" + expiration_date.split('/')[1],
            card_type=card_type,
            cvv2=cvv2,
            card_holder=card_holder
        )

        # Save selected squares to database
        if donation_succeeded and selected_squares:
            for square in selected_squares:
                row, column = square  # Unpack the tuple
                TakenSquare.objects.create(
                    first_name=form_data['first_name'],
                    last_name=form_data['last_name'],
                    display_name=form_data['display_name'],
                    email=form_data['email'],
                    row=row,
                    column=column
                )
        
        # Redirect or render a response
        if donation_succeeded:
            try:
                del request.session['form_data']
            except KeyError:
                logger.error('Error deleting form_data from session.')
            return redirect('success_page')
        else: 
            context['retry_payment'] = True
            return render(request, 'payment_page.html', context)
    else:
        return render(request, 'payment_page.html', context)

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