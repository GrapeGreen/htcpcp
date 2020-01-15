import sys


allowed_methods = frozenset(['BREW', 'WHEN'])
allowed_commands = frozenset(['start', 'stop'])
allowed_headers = frozenset(['Accept-Additions', 'Host'])
allowed_additions = frozenset([
    'Cream', 'Half-and-half', 'Whole-milk', 'Part-Skim', 'Skim', 'Non-Dairy',
    'Vanilla', 'Almond', 'Raspberry', 'Chocolate',
    'Whisky', 'Rum', 'Kahlua', 'Aquavit'
])
http_code_mappings = {
    200: 'OK',
    202: 'Accepted',
    201: 'Created',
    400: 'Bad Request',
    418: 'I"m a Teapot',
    501: 'Not Implemented',
    503: 'Service Unavailable'
}


def parse(request):
    parsed_request = {}
    method_line, *headers = filter(None, request.split('\n'))

    # Process method line.
    method, beverage, htcpcp = map(lambda x: x.strip(), method_line.split())
    if method not in allowed_methods:
        return parsed_request, 501
    if beverage != '/tea':
        return parsed_request, 418
    if htcpcp != 'HTCPCP/1.0':
        return parsed_request, 501
    parsed_request['method'] = method
    parsed_request['beverage'] = beverage
    parsed_request['htcpcp'] = htcpcp

    if method == 'BREW':
        headers, command = headers[:-1], headers[-1]
        if not command or command not in allowed_commands:
            return parsed_request, 400
        parsed_request['command'] = command
    for header in headers:
        name, contents = map(lambda x: x.strip(), header.split(':', maxsplit=1))
        if name not in allowed_headers:
            return parsed_request, 501
        contents_list = [x.strip() for x in contents.split(';')]
        parsed_request[name] = contents_list
    return parsed_request, 200


def create_http_line(status):
    return '{} {} {}'.format('HTCPCP/1.0', status, http_code_mappings[status])
