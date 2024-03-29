from server import app
from layouts.main import main_layout

# Include Bootstrap CSS
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"})

# Include layout
app.layout = main_layout
app.config.prevent_initial_callbacks = 'initial_duplicate'
app.config['suppress_callback_exceptions'] = True
# Include callbacks (Needs to be assigned after setting layout up)
from callbacks.main import *

# Initializing app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
