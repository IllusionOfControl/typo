from monologue import create_app
from monologue.models import db

app = create_app()
app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}