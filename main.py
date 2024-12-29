from wsgiref.simple_server import make_server
from pytz import timezone, all_timezones
from datetime import datetime
import json
from urllib.parse import parse_qs

# Настройки временной зоны сервера
SERVER_TZ = "Etc/GMT-7"

def parse_date(date_str):
    date_formats = [
        '%Y-%m-%d %H:%M:%S',    # 2024-12-29 15:30:00
        '%d.%m.%Y %H:%M:%S',    # 29.12.2024 15:30:00
        '%I:%M%p %Y-%m-%d',     # 03:30PM 2024-12-29
        '%m.%d.%Y %H:%M:%S',    # 12.29.2024 15:30:00
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None  # Если ни один формат не подошёл

def get_current_time(tz_name):
    try:
        tz = timezone(tz_name)
    except Exception as exs :
        return None
    return datetime.now(tz)

def time_handler(env):
    path = env['PATH_INFO']
    method = env['REQUEST_METHOD']
    query = parse_qs(env['QUERY_STRING'])
    tz_param = query.get('tz', [SERVER_TZ])[0]

    # GET /
    if method == 'GET' and path == '/':
        current_time = get_current_time(SERVER_TZ)
        body = f"<html><body><h1>Current time (server zone): {current_time}</h1></body></html>"

        return body.encode('utf-8'), "200 OK"

    # GET /<tz name>
    if method == 'GET' and path.startswith('/'):
        tz_name = path.strip('/')
        current_time = get_current_time(tz_name)

        if current_time is None:
            body = f"<html><body><h1>Invalid timezone: {tz_name}</h1></body></html>"
            return body.encode('utf-8'), "400 Bad Request"
        
        
        body = f"<html><body><h1>Current time ({tz_name}): {current_time}</h1></body></html>"
        return body.encode('utf-8'), "200 OK"

    # POST /api/v1/time
    if method == 'POST' and path == '/api/v1/time':
        length = int(env['CONTENT_LENGTH']) if env['CONTENT_LENGTH'] else 0
        body = env['wsgi.input'].read(length).decode('utf-8')
        params = json.loads(body)
        tz_name = params.get('tz', SERVER_TZ)
        current_time = get_current_time(tz_name)

        if current_time is None:
            return json.dumps({"error": f"Invalid timezone: {tz_name}"}).encode('utf-8'), "400 Bad Request"
        
        return json.dumps({"current_time": current_time.strftime('%Y-%m-%d %H:%M:%S')}).encode('utf-8'), "200 OK"

    # POST /api/v1/date
    if method == 'POST' and path == '/api/v1/date':
        length = int(env['CONTENT_LENGTH']) if env['CONTENT_LENGTH'] else 0
        body = env['wsgi.input'].read(length).decode('utf-8')
        params = json.loads(body)
        tz_name = params.get('tz', SERVER_TZ)
        current_time = get_current_time(tz_name)

        if current_time is None:
            return json.dumps({"error": f"Invalid timezone: {tz_name}"}).encode('utf-8'), "400 Bad Request"
        
        return json.dumps({"current_date": current_time.strftime('%Y-%m-%d')}).encode('utf-8'), "200 OK"

    # POST /api/v1/datediff
    if method == 'POST' and path == '/api/v1/datediff':
        length = int(env['CONTENT_LENGTH']) if env['CONTENT_LENGTH'] else 0
        body = env['wsgi.input'].read(length).decode('utf-8')

        params = json.loads(body)
        start = params.get('start')
        end = params.get('end')

        if not start or not end:
            return json.dumps({"error": "Missing 'start' or 'end' parameter"}).encode('utf-8'), "400 Bad Request"

        # Парсим даты
        start_date = parse_date(start['date'])
        end_date = parse_date(end['date'])

        if not start_date or not end_date:
            return json.dumps({"error": "Invalid date format"}).encode('utf-8'), "400 Bad Request"

        # Парсим временные зоны
        start_tz = timezone(start.get('tz', SERVER_TZ))
        end_tz = timezone(end.get('tz', SERVER_TZ))

        # Локализация дат
        start_date = start_tz.localize(start_date)
        end_date = end_tz.localize(end_date)

        # Вычисление разницы
        diff = str(end_date - start_date)
        return json.dumps({"dates_difference": diff}).encode('utf-8'), "200 OK"

    return json.dumps({"error": "Invalid request"}).encode('utf-8'), "400 Bad Request"




def application(env, start_response):
    response, status = time_handler(env)
    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)
    return [response]

if __name__ == "__main__":
    with make_server('', 1337, application) as server:
        print("Serving on port 1337...")
        server.serve_forever()
