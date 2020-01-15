import socket
import sys
import parser
import pot


teapot = pot.Teapot(seconds=10)


def process(request):
    if request['method'] == 'BREW':
        if request['command'] == 'start':
            additions = request.get('Accept-Additions', None)
            status = teapot.brew_start(additions)
            if status != 202:
                return parser.create_http_line(status)
            return '\n'.join(filter(lambda x: x is not None, [
                parser.create_http_line(202),
                'Content-Type: message/teapot',
                '',
                'Your tea is being brewed {}.'.format(
                    '' if additions is None
                    else 'with the following additions: {}.'.format(', '.join(additions))
                ),
                'Come back in {} seconds!'.format(10)
            ]))
        else:
            status = teapot.brew_stop()
            if status != 201:
                return parser.create_http_line(status)
            return '\n'.join([
                parser.create_http_line(201),
                'Content-Type: message/teapot',
                '',
                'Finished brewing your tea. Come and collect it!'
            ])
    elif request['method'] == 'WHEN':
        date = teapot.when()
        return '\n'.join([
            parser.create_http_line(200),
            'Content-Type: message/teapot',
            '',
            'Your tea will be ready at {}'.format(date.ctime()) if date else 'Your tea is ready.'
        ])
    else:
        return parser.create_http_line(501)


def encode(data):
    return '{}\n'.format(data).encode('utf8')


def handle(data):
    request, status = parser.parse(data)
    if status != 200:
        return parser.create_http_line(status)
    return process(request)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 65432))
        s.listen()
        connection, address = s.accept()
        with connection:
            print('Connected to {address}', file=sys.stderr)
            while True:
                data = connection.recv(2048)
                if not data:
                    break
                try:
                    print(data.decode('utf8'), file = sys.stderr)
                    connection.send(encode(handle(data.decode('utf8'))))
                except KeyboardInterrupt as e:
                    break
                except Exception as e:
                    connection.send(encode(parser.create_http_line(400)))


if __name__ == '__main__':
    main()
