from typo import create_app
from typo.models import db

app = create_app()
app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}