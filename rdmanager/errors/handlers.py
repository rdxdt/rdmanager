from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)

# Titles follow RFC 9110 (and RFC 2324, 4918, 6585, 7725 for the extension codes),
# which differ from some of Werkzeug's legacy names such as 413 and 422
HTTP_ERRORS = {
    400: (
        "Bad Request",
        "The request could not be understood. Please check it and try again.",
    ),
    401: ("Unauthorized", "You need to log in to access this page."),
    403: ("Forbidden", "You don't have permission to access this page."),
    404: ("Not Found", "The page you are looking for doesn't exist or was moved."),
    405: ("Method Not Allowed", "This action is not supported on this page."),
    406: (
        "Not Acceptable",
        "The page can't be shown in a format your browser accepts.",
    ),
    408: ("Request Timeout", "The request took too long to arrive. Please try again."),
    409: (
        "Conflict",
        "The request conflicts with the current state of the data. Please reload and try again.",
    ),
    410: ("Gone", "This page is no longer available."),
    411: ("Length Required", "The request is missing its content length."),
    412: (
        "Precondition Failed",
        "The data changed since you loaded it. Please reload and try again.",
    ),
    413: ("Content Too Large", "The data you sent is too large."),
    414: ("URI Too Long", "The address you requested is too long."),
    415: ("Unsupported Media Type", "The type of data you sent is not supported."),
    416: (
        "Range Not Satisfiable",
        "The requested part of the content is not available.",
    ),
    417: (
        "Expectation Failed",
        "The server can't meet the requirements of the request.",
    ),
    418: ("I'm a Teapot", "The server refuses to brew coffee because it is a teapot."),
    421: (
        "Misdirected Request",
        "The request was sent to a server that can't answer it.",
    ),
    422: (
        "Unprocessable Content",
        "The data you sent could not be processed. Please check it and try again.",
    ),
    423: ("Locked", "This resource is locked at the moment."),
    424: ("Failed Dependency", "The request failed because a related request failed."),
    428: (
        "Precondition Required",
        "The request must be conditional to avoid conflicting changes.",
    ),
    429: (
        "Too Many Requests",
        "You made too many requests. Please wait a moment and try again.",
    ),
    431: ("Request Header Fields Too Large", "The request headers are too large."),
    451: (
        "Unavailable For Legal Reasons",
        "This page is unavailable for legal reasons.",
    ),
    500: (
        "Internal Server Error",
        "Something went wrong on our side. Please try again later.",
    ),
    501: ("Not Implemented", "This feature is not available yet."),
    502: (
        "Bad Gateway",
        "The server received an invalid response from an upstream server. Please try again later.",
    ),
    503: (
        "Service Unavailable",
        "The service is temporarily unavailable. Please try again later.",
    ),
    504: (
        "Gateway Timeout",
        "An upstream server took too long to respond. Please try again later.",
    ),
    505: (
        "HTTP Version Not Supported",
        "Your browser uses an HTTP version the server doesn't support.",
    ),
}


def handle_error(error):
    title, message = HTTP_ERRORS[error.code]
    # Keeps headers such as Allow (405), WWW-Authenticate (401) and Retry-After (429, 503)
    return (
        render_template(
            "error.html",
            title=title,
            errorcode=error.code,
            errormessage=message,
        ),
        error.code,
        error.get_headers(),
    )


# Flask only accepts handlers for codes that Werkzeug implements, so codes such as
# 402 or 511 can't be registered here
for code in HTTP_ERRORS:
    errors.app_errorhandler(code)(handle_error)
