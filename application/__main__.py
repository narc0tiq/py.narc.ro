from application import app

app.run(host=app.config['LISTEN_INTERFACE'],
        debug=app.config['DEBUG'],
        port=8081,
        use_evalex=app.config['DEBUG_INTERACTIVE'])
