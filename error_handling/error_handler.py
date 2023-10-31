
def handle_error(error_msg, status_code):
    status_code = status_code 

    error_data = {
        'error': {
            'error_code': status_code,
            'error_message': error_msg,
        }
    }

    return error_data
