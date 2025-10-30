from flask import Flask, jsonify, current_app
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)

DEFAULT_DB = Path(__file__).resolve().parents[1] / 'mercado_campesino' / 'db.sqlite3'
app.config['DB_PATH'] = os.environ.get('PRODUCTS_DB_PATH', str(DEFAULT_DB))
app.config['BASE_URL'] = os.environ.get('PRODUCTS_BASE_URL', 'http://localhost:8000')


def get_db_connection(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)


@app.route('/api/productos', methods=['GET'])
def productos_disponibles():
    """Devuelve la lista de productos con stock > 0 en formato JSON.

    Cada item contiene: id, nombre, stock, url (enlace al detalle en la app Django).
    """
    db_path = current_app.config['DB_PATH']
    base_url = current_app.config['BASE_URL'].rstrip('/')

    if not os.path.exists(db_path):
        return jsonify({'error': f'Database file not found at {db_path}'}), 500

    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, stock FROM productos_producto WHERE stock > 0")
        rows = cur.fetchall()

        productos = []
        for r in rows:
            prod_id, nombre, stock = r
            url = f"{base_url}/producto/{prod_id}/"
            productos.append({
                'id': prod_id,
                'nombre': nombre,
                'stock': stock,
                'url': url
            })

        return jsonify({'count': len(productos), 'productos': productos})

    finally:
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
