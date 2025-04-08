from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Update if needed
        password="",  # Add your MySQL password if required
        database="crypto_votes"
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM votes")
    coins = cursor.fetchall()

    # Get total votes
    total_votes = sum(coin['votes'] for coin in coins)

    # Get most popular coin
    top_coin = max(coins, key=lambda x: x['votes']) if coins else None

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

if __name__ == '__main__':
    app.run(debug=True)
