from nicegui import app, ui
from pages.trello import trello

app.on_startup(trello)


ui.run(title='TrelloPy', language='es', port=443, favicon='img/favicon.png', dark=False, fastapi_docs=True, reload=True, on_air=True)