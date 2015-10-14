from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader


def index(request):

    errors = []

    # pressing digit
    if  'digit' in request.GET:
        previous_button = request.GET['previous_button']
        current_button = request.GET['digit']

        # the digit you press
        digit = request.GET['digit']
        reset_screen = request.GET['reset_screen']

        # need to reset the screen
        if reset_screen == 'True':
            # set the reset_screen to be False
            reset_screen = "False"

            # change the screen
            screen = digit

            previoius_digit = request.GET['previous_digit']
            operation = request.GET['operation']
            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen' : reset_screen, 'exception': 'False', 'previous_button': current_button}
            return render(request, 'cal/main_page.html', context)

        # do not need to reset the screen, join the digit in the screen
        else:
            screen = request.GET['screen']
            # join the string to change the screen
            screen = str(screen) + str(digit)

            previoius_digit = request.GET['previous_digit']
            operation = request.GET['operation']
            reset_screen = request.GET['reset_screen']
            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': current_button}
            return render(request, 'cal/main_page.html', context)

    # pressing a operator
    elif 'operator' in request.GET:
        previous_button = request.GET['previous_button']
        current_button = request.GET['operator']

        # there appears exception and then press operator
        if request.GET['exception'] == 'True':
            previous_digit = 0
            operation = "None"
            screen = request.GET['screen']
            reset_screen = "True"
            exception = request.GET['exception']
            context = {'previous_digit': previous_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button': current_button}
            return render(request, 'cal/main_page.html', context)

        print('********************************')

        print('check the previous button')
        print(previous_button)

        print('********************************')


        # the previous button also is a operator
        if check_if_operator(previous_button):
            previous_digit = request.GET['screen']
            operation = current_button
            screen = request.GET['screen']
            reset_screen = 'True'
            exception = 'False'
            context = {'previous_digit': previous_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button' : current_button }


        current_operator = current_button
        previoius_digit = request.GET['previous_digit']
        operation = request.GET['operation']
        screen = request.GET['screen']
        reset_screen = "True"

        print('*****************************^^^^^^^^^')
        print(previoius_digit)
        print(operation)
        print(screen)
        print('*****************************^^^^^^^^^')

        # there is no operation before
        if operation == "None":
            previoius_digit = screen
            operation = current_operator
            screen = screen
            reset_screen = 'True'

            print('*****************************')
            print(previoius_digit)
            print(operation)
            print(screen)
            print('*****************************')

            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen' : screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': current_button}
            return render(request, 'cal/main_page.html', context)

        if operation == '+':
            cal_result = int(previoius_digit) + int(screen)
        elif operation == '-':
            cal_result = int(previoius_digit) - int(screen)
        elif operation == '*':
            cal_result = int(previoius_digit) * int(screen)
        elif operation == '/':
            if screen == "0":
                errors.append('Can not divide 0.')
                print("there is an error about zero.")


                previous_button = current_operator

                context = {'previous_digit' : "0", 'operation': 'None', 'screen': errors.pop(), 'reset_screen': 'True', 'exception' : 'True', 'previous_button': previous_button}
                return render(request, 'cal/main_page.html', context)
            else:
                cal_result = int(previoius_digit) / int(screen)

        previoius_digit = cal_result
        operation = current_operator
        screen = cal_result
        reset_screen = 'True'
        exception = 'False'
        previous_button = current_operator
        context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button': previous_button}
        return render(request, 'cal/main_page.html', context)


    # pressing a = operator
    elif 'equal' in request.GET:
        previoius_digit = request.GET['previous_digit']
        operation = request.GET['operation']
        screen = request.GET['screen']

        previous_button = '='

        if operation == '+':
            cal_result = int(previoius_digit) + int(screen)
            context = {'previous_digit': cal_result, 'operation': 'None', 'screen': cal_result, 'reset_screen': 'True', 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

        elif operation == '-':
            cal_result = int(previoius_digit) - int(screen)
            context = {'previous_digit': cal_result, 'operation': 'None', 'screen': cal_result, 'reset_screen': 'True', 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

        elif operation == '*':
            cal_result = int(previoius_digit) * int(screen)
            context = {'previous_digit': cal_result, 'operation': 'None', 'screen': cal_result, 'reset_screen': 'True', 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

        elif operation == '/':
            if screen == "0":
                errors.append('can not divide 0.')
                print("there is an error about zero.")
                previous_button = 'None'

                context = {'previous_digit' : "0", 'operation': 'None', 'screen': errors.pop(), 'reset_screen': 'True', 'exception' : 'True', 'previous_button': previous_button}
                return render(request, 'cal/main_page.html', context)
            else:
                cal_result = int(previoius_digit) / int(screen)
                context = {'previous_digit': cal_result, 'operation': 'None', 'screen': cal_result, 'reset_screen': 'True', 'exception': 'False', 'previous_button': previous_button}
                return render(request, 'cal/main_page.html', context)
        # the operation is None
        else:
            previoius_digit = request.GET['previous_digit']
            operation = 'None'
            screen = request.GET['screen']
            reset_screen = 'True'
            exception = 'False'
            previous_button = '='
            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

    # nothing input in the url
    else:

        # initialization
        previous_digit = 0
        operation = 'None'
        screen = 0
        reset_screen = 'True'
        exception = 'False'
        previous_button = 'None'
        context = {'previous_digit': previous_digit, 'operation': operation, 'screen': screen, 'reset_screen' : reset_screen, 'exception': 'False', 'previous_button': previous_button}
        return render(request, 'cal/main_page.html', context)












'''

    errors = []

    # pressing digit
    if 'digit' in request.GET:

        previous_button = request.GET['digit']

        digit = request.GET['digit']
        reset_screen = request.GET['reset_screen']

        # need to reset the screen
        if reset_screen == 'True':
            reset_screen = "False"
            screen = digit
            previoius_digit = request.GET['previous_digit']
            operation = request.GET['operation']
            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen' : reset_screen, 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

        # do not need to reset the screen, join the digit in the screen
        else:
            screen = request.GET['screen']
            # join the string
            screen = str(screen) + str(digit)
            previoius_digit = request.GET['previous_digit']
            operation = request.GET['operation']
            reset_screen = request.GET['reset_screen']
            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

    # pressing operator
    elif 'operator' in request.GET:

        previous_button = request.GET['previous_button']
        current_button = request.GET['operator']

        # there appears exception and then press operator
        if request.GET['exception'] == 'True':
            previous_digit = 0
            operation = "None"
            screen = request.GET['screen']
            reset_screen = "True"
            exception = request.GET['exception']
            context = {'previous_digit': previous_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button': current_button}
            return render(request, 'cal/main_page.html', context)

        # pressing two operator continuously
        if check_if_operator(previous_button):
            previoius_digit = request.GET['screen']
            # here is important, set the second press as the operation
            operation = current_button
            screen = request.GET['screen']
            reset_screen = "True"
            exception = request.GET['exception']

            print('***********************')
            print(previoius_digit)
            print(screen)
            print('***********************')

            context = {'previous_digit' : previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': exception, 'previous_button' :current_button}
            return render(request, 'cal/main_page.html', context)

        if check_if_is_equal_operator(current_button):
            previous_digit = request.GET['screen']
            operation = 'None'
            screen = request.GET['screen']
            request

        current_operator = request.GET['operator']

        previoius_digit = request.GET['previous_digit']
        operation = request.GET['operation']
        screen = request.GET['screen']
        reset_screen = "True"
        previous_button = 'operator'

        print('*****************************^^^^^^^^^')

        print(previoius_digit)
        print(operation)
        print(screen)
        print('*****************************^^^^^^^^^')

        # there is no operation before
        if operation == "None":
            previoius_digit = screen
            operation = current_operator
            screen = screen
            reset_screen = 'True'
            previous_button = 'operator'

            print('*****************************')
            print("second time")
            print(previoius_digit)
            print(operation)
            print(screen)
            print('*****************************')

            context = {'previous_digit': previoius_digit, 'operation': operation, 'screen' : screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)

        if operation == '+':
            cal_result = int(previoius_digit) + int(screen)
        elif operation == '-':
            cal_result = int(previoius_digit) - int(screen)
        elif operation == '*':
            cal_result = int(previoius_digit) * int(screen)
        elif operation == '/':
            if screen == "0":
                errors.append('can not divide 0.')
                print("there is an error about zero.")
                previous_button = 'None'

                context = {'previous_digit' : "0", 'operation': 'None', 'screen': errors.pop(), 'reset_screen': 'True', 'exception' : 'True', 'previous_button': previous_button}
                return render(request, 'cal/main_page.html', context)
            else:
                cal_result = int(previoius_digit) / int(screen)

        # divide 0 error.
        if current_operator == '=':
            if operation == '/':
                if screen == '0':
                    previous_button = "None"
                    context = {'previous_digit' : "0", 'operation': 'None', 'screen': errors.pop(), 'reset_screen': 'True', 'exception' : 'True', 'previous_button': previous_button}
                    return render(request, 'cal/main_page.html', context)

            previoius_digit = cal_result
            screen = cal_result
            operation = 'None'
            reset_screen = 'True'
            previous_button = "operator"
            context = {'previous_digit' : previoius_digit, 'operation': operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)
        else:
            screen = cal_result
            previoius_digit = cal_result
            operation = current_operator
            reset_screen = 'True'
            previous_button = 'operator'
            context = {'previous_digit' : previoius_digit, 'operation' : operation, 'screen': screen, 'reset_screen': reset_screen, 'exception': 'False', 'previous_button': previous_button}
            return render(request, 'cal/main_page.html', context)



    # nothing to press
    else:
        screen = 0
        previous_digit = screen
        operation = 'None'
        reset_screen = 'True'
        previous_button = 'None'
        context = {'previous_digit': previous_digit, 'operation': operation, 'screen': screen, 'reset_screen' : reset_screen, 'exception': 'False', 'previous_button': previous_button}

        return render(request, 'cal/main_page.html', context)

'''


def check_if_operator(previous_button):
    if previous_button == '+':
        return True
    elif previous_button == '-':
        return True
    elif previous_button == '*':
        return True
    elif previous_button == '/':
        return True
    else:
        return False

def check_if_is_equal_operator(previous_button):
    if previous_button == '=':
        return True
    else:
        return False

def check_if_is_number(previous_button):
    if previous_button == '0':
        return True
    elif previous_button == '1':
        return True
    elif previous_button == '2':
        return True
    elif previous_button == '3':
        return True
    elif previous_button == '4':
        return True
    elif previous_button == '5':
        return True
    elif previous_button == '6':
        return True
    elif previous_button == '7':
        return True
    elif previous_button == '8':
        return True
    elif previous_button == '9':
        return True
    else:
        return False