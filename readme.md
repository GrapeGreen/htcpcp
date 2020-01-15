# HTCPCP

## Установка:

1. Склонировать репозиторий

2. `docker-compose up --build`

Сервер слушает порт 65432.

## Примеры команд:

1.

        BREW /coffee HTCPCP/1.0
        Host: localhost

        start

        HTCPCP/1.0 418 I'm a teapot
   
2.

        BREW /tea HTCPCP/1.0
        Host: localhost
        Accept-Additions: milk;sugar

        start

        HTCPCP/1.0 202 Accepted
        Content-Type: message/teapot

        Your tea is being brewed with the following additions: milk, sugar.
        Come back in 10 seconds!

3.

        http
        BREW /tea HTCPCP/1.0
        Host: localhost

        stop

        HTCPCP/1.0 201 Created
        Content-Type: message/teapot

        Finished brewing you tea. Come and collect it!

4.

        http
        WHEN /tea HTCPCP/1.0
        Host: localhost

        HTCPCP/1.0 200 OK
        Content-Type: message/teapot

        Your tea is ready.
