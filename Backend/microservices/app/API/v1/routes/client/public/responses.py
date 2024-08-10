responses_login: dict = {

    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "INCORRECT_PASSWORD": {
                        "info": "Incorrect password.",
                        "status": "no",
                        "type": "INCORRECT_PASSWORD"
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "info": "No se encontró ningún usuario con el email: exampleandrin@gmail.com",
                    "status": "ok",
                    "type": "NO_FOUND_USER"
                }
            }
        }
    }
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "token_id": "...",
                    "token_data": "..."
                },
                "example": {
                    "token_id": "...",
                    "token_data": "..."
                }
            }
        }
    }

}


