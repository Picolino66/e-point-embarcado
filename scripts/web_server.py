import picoweb
from machine import Pin

def host_server(event=None, callback=None):
    app = picoweb.WebApp(__name__)
    content = []

    @app.route("/cadastro")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from resp.awrite("Pagina que solicitara ao membro para que se aproxime o cartao")
        yield from app.render_template(resp, "info.tpl", (req,))


    @app.route("/")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from resp.awrite("Pagina em que se fara a seleçao dos membros cadastrados")
        yield from app.render_template(resp, "index.tpl", (req,))

    import logging as logging
    logging.basicConfig(level=logging.INFO)

    app.run(debug=True, host='0.0.0.0')