import json
from context import EasydbException

## called from easydb

def easydb_server_start(easydb_context):
    # called when server starts (just once)
    logger = easydb_context.get_logger('example-plugin')
    logger.debug('server_start')
    logger.debug('instance information: {0}'.format(json.dumps(easydb_context.get_instance())))
    easydb_context.register_callback('api', { 'name': 'echo', 'callback': 'echo'})
    easydb_context.register_callback('api', { 'name': 'config', 'callback': 'config'})
    easydb_context.register_callback('api', { 'name': 'session', 'callback': 'session'})
    easydb_context.register_callback('api', { 'name': 'tmp', 'callback': 'tmp'})
    easydb_context.register_callback('api', { 'name': 'instance', 'callback': 'instance'})

def config(easydb_context, parameters):
    return json_response(easydb_context.get_config())

def session(easydb_context, parameters):
    return json_response(easydb_context.get_session())

def tmp(easydb_context, parameters):
    tmp_dir = easydb_context.get_temp_dir()
    return text_response('temp dir: {0}'.format(tmp_dir))

def instance(easydb_context, parameters):
    instance = easydb_context.get_instance()
    return json_response(easydb_context.get_instance())

def echo(easydb_context, parameters):
    status_code = 200
    content_type = '<undefined>'
    lines = []

    lines.append('*** Request Information ***')
    lines.append('')
    lines.append(u'{0} {1}'.format(parameters['method'], parameters['path']))
    query_string = parameters['query_string']
    if len(query_string) > 0:
        lines.append('Query String Parameters:')
        for part in query_string.split('&'):
            part_parts = part.split('=')
            key = part_parts[0]
            if len(part_parts) > 1:
                value = part_parts[1]
            else:
                value = '<undefined>'
            lines.append(u'* {0} = {1}'.format(key, value))
            if key == 'status_code':
                status_code = int(value)
    else:
        lines.append('Query String: <empty>')
    lines.append('')
    lines.append('Headers:')
    for key, value in parameters['headers'].items():
        lines.append('* {0}: {1}'.format(key, value))
        if key.lower() == 'content-type':
            content_type = value
    lines.append('')
    body = parameters['body']
    if len(body) > 0:
        if 'text' in content_type or 'json' in content_type:
            lines.append('Body:')
            lines.append('')
            lines.append(body)
        else:
            lines.append('Body: {0} bytes'.format(len(body)))
    else:
            lines.append('Body: none')
    lines.append('')
    return text_response('\n'.join(lines), status_code=status_code)

def json_response(js):
    return {
        "status_code": 200,
        "body": json.dumps(js, indent=4),
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        }
    }

def text_response(text, status_code=200):
    return {
        "status_code": status_code,
        "body": text,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8"
        }
    }

