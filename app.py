from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        user='root',
        password='Itsbryan500!!!',
        database='cryptodb',
        unix_socket='/tmp/mysql.sock',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM votes")
    coins = cursor.fetchall()

    total_votes = sum(coin['vote_count'] for coin in coins)
    top_coin = max(coins, key=lambda x: x['vote_count']) if coins else None

    cursor.close()
    conn.close()
    return render_template('index.html', coins=coins, total_votes=total_votes, top_coin=top_coin)

@app.route('/vote', methods=['POST'])
def vote():
    coin_id = request.form['coin_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE votes SET vote_count = vote_count + 1 WHERE id = %s", (coin_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE votes SET vote_count = 0")
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)