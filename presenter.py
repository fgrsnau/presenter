#!/usr/bin/env python3

import dbus
import flask
import os.path
import subprocess
import time
import urllib.request

app = flask.Flask(__name__)

@app.route('/')
def index():
    return '''
        <!DOCTYPE html5>
        <html>
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Presenter</title>
                <style type="text/css">
                  body {
                    font-size: 20pt;
                  }
                  button {
                    padding: 1em;
                    font-size: 200%;
                  }
                  button#prev {
                    position: absolute;
                    left: 0px;
                    width: 50%;
                  }
                  button#next {
                    position: absolute;
                    right: 0px;
                    width: 50%;
                  }
                </style>
                <script type="text/javascript" src="/jquery.js"></script>
                <script type="text/javascript">
                    function call(msg) {
                        $.post('/' + msg)
                    }
                </script>
            </head>
            <body>
                <button id="prev" onclick="javascript:call('prev')">← Prev</button>
                <button id="next" onclick="javascript:call('next')">Next →</button>
            </body>
        </html>
    '''

@app.route('/jquery.js')
def js():
    return flask.send_file('jquery.js')

@app.route('/prev', methods=['POST'])
def prev():
    global dbus1, dbus2
    dbus1.slotPreviousPage()
    dbus2.slotPreviousPage()
    return ''

@app.route('/next', methods=['POST'])
def next():
    global dbus1, dbus2
    dbus1.slotNextPage()
    dbus2.slotNextPage()
    return ''

if __name__ == '__main__':
    if not os.path.isfile('jquery.js'):
        urllib.request.urlretrieve('https://code.jquery.com/jquery-3.1.1.min.js', 'jquery.js')

    okular1 = subprocess.Popen(['okular', 'presentation.pdf'], stdin=subprocess.DEVNULL)
    time.sleep(1)
    okular2 = subprocess.Popen(['okular', 'notes.pdf'], stdin=subprocess.DEVNULL)
    time.sleep(1)

    session = dbus.SessionBus()

    dbus1 = session.get_object('org.kde.okular-{}'.format(okular1.pid), '/okular')
    dbus2 = session.get_object('org.kde.okular-{}'.format(okular2.pid), '/okular')

    for obj in (dbus1, dbus2):
        obj.goToPage(dbus.UInt32(1))

    app.run(host='0.0.0.0')
