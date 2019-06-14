#Arquivo responsavel por controlar as rotas do servidor do ESP
import picoweb
import machine

def host_server(event=None, callback=None):
    app = picoweb.WebApp(__name__)
    matricula = 0

    @app.route("/")
    def index(req, resp):
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "matricula.tpl", (req,))

    @app.route("/cadastro_efetuado")
    def index(req, resp):
        if req.method == "POST":
            yield from picoweb.start_response(resp)
            yield from app.render_template(resp, "cadastro_efetuado.tpl", (req,))
        else:
            yield from app.render_template(resp, "404.tpl", (req,))

        
    @app.route("/aproxime_cartao")
    def index(req, resp):
        if req.method == "POST":
            yield from req.read_form_data()
            yield from picoweb.start_response(resp)
            yield from app.render_template(resp, "aproxime_cartao.tpl", (req,))
            nonlocal matricula
            matricula = req.form["matricula"]
            callback.clear()
            callback.set(matricula) #Seta o _cad passando a matricula
        else:
            yield from app.render_template(resp, "404.tpl", (req,))

    @app.route("/server_off")
    def index(req, resp):
        if req.method == "POST":
            yield from picoweb.start_response(resp)
            #yield from resp.awrite("Servidor Desligado!!")
            callback.clear()
            event.clear()
            machine.reset()
        else:
            yield from app.render_template(resp, "404.tpl", (req,))

    import logging as logging
    logging.basicConfig(level=logging.INFO)

    app.run(debug=True, host='0.0.0.0')