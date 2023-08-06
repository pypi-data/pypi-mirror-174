from handler_app import plh


@plh.get("/error", errors=[(418, ValueError)])
def error_skip():
    raise ValueError("nope")
