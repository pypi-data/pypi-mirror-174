from sys import argv

from core.app import App

app = App()
app.add_session(argv)
app.run()
