# TODO: Fix this hardcoding
DEFAULT_CMD = ['python', '-m', 'jhsingle_native_proxy.main', '--authtype=none']

EXAMPLES_PATH = {
    "panel": "/Users/aktech/quansight/jhub-apps/jhub_apps/examples/panel_basic.py",
    "streamlit": "/Users/aktech/quansight/jhub-apps/jhub_apps/examples/streamlit_app.py"
}

base_url = "http://127.0.0.1:8000"
origin_host = "localhost:8000"


COMMANDS = {
    'voila': {
        'args': ['--destport=0', 'python3', '{-}m', 'voila', f'{EXAMPLES_PATH.get("voila")}',
                 '{--}port={port}',
                 '{--}no-browser',
                 '{--}Voila.base_url={base_url}/',
                 '{--}Voila.server_url=/',
                 '{--}Voila.ip=0.0.0.0',
                 '{--}Voila.tornado_settings', 'allow_origin={origin_host}',
                 '--progressive',
                 '--ready-check-path=/voila/static/'
                 ],
    },
    'streamlit': {
        'args': ['--destport=0', 'streamlit', 'run', f'{EXAMPLES_PATH.get("streamlit")}',
                 '{--}server.port={port}',
                 '{--}server.headless=True',
                 '{--}browser.serverAddress='+f'{origin_host}',
                 '{--}browser.gatherUsageStats=false'],
        'debug_args': [],
    },
    'plotlydash': {
        'args': ['--destport=0', 'python3', '{-}m', 'plotlydash_tornado_cmd.main', f'{EXAMPLES_PATH.get("plotlydash")}',
                 '{--}port={port}'],
        'env': {'DASH_REQUESTS_PATHNAME_PREFIX': '{base_url}/'}
    },
    'bokeh': {
        'args': ['--destport=0', 'python3', '{-}m', 'bokeh_root_cmd.main', f'{EXAMPLES_PATH.get("bokeh")}',
                 '{--}port={port}',
                 '{--}allow-websocket-origin={origin_host}',
                 '{--}prefix={base_url}',
                 '--ready-check-path=/ready-check']
    },
    'panel': {
        'args': ['--destport=0', 'python', '{-}m', 'bokeh_root_cmd.main', f'{EXAMPLES_PATH.get("panel")}',
                 '{--}port={port}',
                 '{--}debug',
                 '{--}allow-websocket-origin='+f'{origin_host}',
                 '{--}server=panel',
                 '{--}prefix='+f'{base_url}',
                 '--ready-check-path=/ready-check']
    },
    'rshiny': {
        'args': ['--destport=0', 'python3', '{-}m', 'rshiny_server_cmd.main', f'{EXAMPLES_PATH.get("rshiny")}',
                 '{--}port={port}']
    }

}