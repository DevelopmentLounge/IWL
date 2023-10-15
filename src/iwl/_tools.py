from flask import Flask
from . import parse
import traceback
import os


app = Flask("iwl.development-sample-server")
env = ""

mod_times = {}


def run_sample_server(host: str = "127.0.0.1", port: int = 8080, env_path: str = "./"):
    if not os.path.exists(os.path.join(env_path, ".converted")):
        os.mkdir(os.path.join(env_path, ".converted"))
    global env
    env = env_path
    app.run(host, port)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def any_route(path: str):
    if not path:
        path = "index.iwl"
    if "." in path:
        path = path.split(".")[0] + ".iwl"
    else:
        path += ".iwl"

    try:
        return load_file(path)
    except:
        if os.path.exists(os.path.join(env, ".converted", path.replace(".iwl", ".html"))):
            os.remove(os.path.join(env, ".converted", path.replace(".iwl", ".html")))
        mod_times.pop(path)
        error = traceback.format_exc().replace('\n', '<br>')
        if os.path.exists(os.path.join(env, "500.iwl")):
            try:
                return load_file("500.iwl")
            except:
                l_error = traceback.format_exc().replace('\n', '<br>')
                return f"<body><h1>500 Internal server error while loading internal server error page</h1>" \
                       f"<br>Loader error: {l_error}<br><br><br><br>Page error: {error}</body>"
        else:
            return f"<body><h1>500 Internal server error</h1><br>{error}</body>"


def load_file(path):
    if not os.path.exists(os.path.join(env, path)):
        if os.path.exists(os.path.join(env, "404.iwl")):
            return load_file("404.iwl")
        else:
            return f"<body><h1>404 Page not found</h1></body>"
    else:
        mtime = os.path.getmtime(os.path.join(env, path))
        if mod_times.get(path, 0) != mtime:
            mod_times[path] = mtime
            with open(os.path.join(env, ".converted", path.replace(".iwl", ".html")), "w") as f:
                f.write(parse.to_html(os.path.join(env, path)))
                f.close()
        return open(os.path.join(env, ".converted", path.replace(".iwl", ".html")), "r").read()
