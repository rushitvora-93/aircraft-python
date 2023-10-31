
def handle_response(msg, status, code, total):

    response_data = {
        "result": {
            "status": status,
            "code": code,
            "message": msg,
            "total": total
        }
    }

    return response_data