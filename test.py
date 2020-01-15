import unittest
import parser
import pot
import server
import time


class TeapotTest(unittest.TestCase):
    def setUp(self):
        self.teapot = pot.Teapot(seconds=1)

    def test_brew_tea_with_manual_stop(self):
        status = self.teapot.brew_start(additions=None)
        self.assertEqual(status, 202)
        self.assertIsNotNone(self.teapot.when())
        status = self.teapot.brew_stop()
        self.assertEqual(status, 201)
        self.assertIsNone(self.teapot.when())

    def test_brew_tea_with_timeout(self):
        self.teapot.brew_start(additions=None)
        self.assertIsNotNone(self.teapot.when())
        time.sleep(1)
        self.assertIsNone(self.teapot.when())

    def test_brew_second_tea(self):
        status = self.teapot.brew_start(additions=None)
        self.assertEqual(status, 202)
        status = self.teapot.brew_start(additions=None)
        self.assertEqual(status, 503)

    def test_stop_brewing_absent_tea(self):
        status = self.teapot.brew_stop()
        self.assertEqual(status, 400)


class ParserTest(unittest.TestCase):
    def test_parser_brew_coffee(self):
        request = '\n'.join([
            'BREW /coffee HTCPCP/1.0',
            'Host: localhost',
            '',
            'start'
        ])
        _, status = parser.parse(request)
        self.assertEqual(status, 418)

    def test_parser_brew_tea(self):
        request = '\n'.join([
            'BREW /tea HTCPCP/1.0',
            'Host: localhost',
            '',
            'start'
        ])
        _, status = parser.parse(request)
        self.assertEqual(status, 200)

    def test_parser_when(self):
        request = '\n'.join([
            'WHEN /tea HTCPCP/1.0',
            'Host: localhost',
        ])
        _, status = parser.parse(request)
        self.assertEqual(status, 200)

    def test_parser_post(self):
        request = '\n'.join([
            'POST /tea HTCPCP/1.0',
            'Host: localhost',
        ])
        _, status = parser.parse(request)
        self.assertEqual(status, 501)


class ServerTest(unittest.TestCase):
    def test_brew_tea(self):
        start_request = 'BREW /tea HTCPCP/1.0\nHost: localhost\nAccept-Additions: milk;sugar\nstart'
        response = server.handle(start_request)
        self.assertIn('with the following additions: milk, sugar', response)
        when_request = 'WHEN /tea HTCPCP/1.0\nHost: localhost'
        response = server.handle(when_request)
        self.assertIn('will be ready at', response)
        stop_request = 'BREW /tea HTCPCP/1.0\nHost: localhost\n\nstop'
        server.handle(stop_request)
        response = server.handle(when_request)
        self.assertIn('is ready', response)


if __name__ == '__main__':
    unittest.main()
