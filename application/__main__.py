from application.app import app

app.run(debug=app.config['DEBUG'], port=8081, use_evalex=app.config['DEBUG_INTERACTIVE'])
