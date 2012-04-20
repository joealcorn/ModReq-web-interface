from flask import Flask, render_template, g, redirect, url_for, flash
import sqlite3, datetime, time, pretty_age


app = Flask(__name__)
app.config.from_pyfile('config.py')

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()
    
@app.teardown_request
def teardown_request(exception):
    g.db.close()
    

@app.route('/')
def index():
    start = time.time()
    cur = g.db.execute('select id, player_name, assigned_mod, request_time, request, close_message, status from modreq_requests order by id desc limit ?', [app.config['REQ_LIMIT']])
    requests = [dict(id=row[0], player=row[1], mod=row[2], time=row[3], request=row[4], comment=row[5], status=row[6]) for row in cur.fetchall()]
    requests = format(requests)

    return render_template('show.html', requests=requests, elapsed=(time.time() - start))

@app.route('/player/<username>/')
def player(username):
    start = time.time()
    cur = g.db.execute('select id, player_name, assigned_mod, request_time, request, close_message, status from modreq_requests where lower(player_name) = ? order by id desc limit ?', [username.lower()], [app.config['REQ_LIMIT']])
    requests = [dict(id=row[0], player=row[1], mod=row[2], time=row[3], request=row[4], comment=row[5], status=row[6]) for row in cur.fetchall()]
    if requests == []:
        flash("That user hasn't made any requests")
        return redirect(url_for('index'))

    requests = format(requests)

    return render_template('show.html', requests=requests, elapsed=(time.time() - start))

@app.route('/mod/<username>/')
def moderator(username):
    start = time.time()
    cur = g.db.execute('select id, player_name, assigned_mod, request_time, request, close_message, status from modreq_requests where lower(assigned_mod) = ? limit 0, 150 order by id desc limit ?', [username.lower()], [app.config['REQ_LIMIT']])
    requests = [dict(id=row[0], player=row[1], mod=row[2], time=row[3], request=row[4], comment=row[5], status=row[6]) for row in cur.fetchall()]
    if requests == []:
        flash("That user hasn't handled any requests")
        return redirect(url_for('index'))

    requests = format(requests)

    return render_template('show.html', requests=requests, elapsed=(time.time() - start))

def format(requests):
    for request in requests:
        if request['status'] == 2:
            request['status'] = 'Open'
        elif request['status'] == 1:
            request['status'] = 'Claimed'
        elif request['status'] == 0:
            request['status'] = 'Closed'
        if request['comment'] == None:
            request['comment'] = ''
        request['time'] = pretty_age.get_age((datetime.datetime.fromtimestamp(request['time']/1000)))
    return requests

@app.errorhandler(404)
def error_404(error):
    flash("404: That page could not be found.")
    return index(), 404

    
if __name__ == '__main__':
    app.run()
