import json
from Physics import Database
from game_manager import initialize_table_with_balls, save_game_state, save_svg
import math
import random
import sqlite3
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse, parse_qsl
import cgi
import os
import Physics
from phylib import PHYLIB_BALL_RADIUS, PHYLIB_HOLE_RADIUS, PHYLIB_TABLE_LENGTH, PHYLIB_TABLE_WIDTH
import sqlite3

def nudge():
    return random.uniform( -1.5, 1.5 );

game = None
table = None

class MyHandler(BaseHTTPRequestHandler):
    def _init_(self, *args, **kwargs):
        self.db_conn = sqlite3.connect('poolgame.db')
        self.db_cursor = self.db_conn.cursor()
        super()._init_(*args, **kwargs)

    def serve_static_file(self, path, content_type):
        try:
            with open(path.lstrip('/'), 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-length', len(content))
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            print(f"Error serving file {path}: {e}")
            self.send_error(500, "Internal Server Error")

    def serve_svg(self, svg_filename):
        try:
            with open(svg_filename, 'r') as svg_file:
                svg_content = svg_file.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(bytes(svg_content, 'utf-8'))
        except FileNotFoundError:
            self.send_error(404, f'SVG file not found: {svg_filename}')
        except Exception as e:
            print(f"Error serving SVG file {svg_filename}: {e}")
            self.send_error(500, 'Internal Server Error')

    def serve_svg_content(self, svg_content):
        # Serve raw SVG XML content directly, without expecting a file
        self.send_response(200)
        self.send_header('Content-type', 'image/svg+xml')
        self.end_headers()
        self.wfile.write(svg_content.encode('utf-8'))

    def generate_svg_from_state(game_state):
        svg_header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="700" height="1375" viewBox="0 0 1350 2700">"""
        svg_footer = "</svg>"

        svg_content = ""
        for obj in game_state:
            if obj["type"] == "StillBall" or obj["type"] == "RollingBall":
                svg_content += '<circle cx="{}" cy="{}" r="{}" fill="{}" />\n'.format(
                    obj["position"]["x"], obj["position"]["y"], PHYLIB_BALL_RADIUS, obj["color"]
                )
            elif obj["type"] == "Hole":
                svg_content += '<circle cx="{}" cy="{}" r="{}" fill="black" />\n'.format(
                    obj["position"]["x"], obj["position"]["y"], PHYLIB_HOLE_RADIUS
                )
            elif obj["type"] == "HCushion":
                svg_content += '<rect x="{}" y="{}" width="{}" height="{}" fill="darkgreen" />\n'.format(
                    0, obj["y"], PHYLIB_TABLE_WIDTH, 25  # Assuming the cushion thickness is 25 units
                )
            elif obj["type"] == "VCushion":
                svg_content += '<rect x="{}" y="{}" width="{}" height="{}" fill="darkgreen" />\n'.format(
                    obj["x"], 0, 25, PHYLIB_TABLE_LENGTH  # Assuming the cushion thickness is 25 units
                )

        svg_string = svg_header + svg_content + svg_footer
        return svg_string

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/shoot.html':
            self.serve_static_file('shoot.html', 'text/html')
        elif parsed_path.path.startswith('/game'):
            # Extract table_id from the query parameters
            query_params = parse_qs(parsed_path.query)
            table_id = query_params.get('table_id', [None])[0]
            if table_id:
                db = Database()
                table_id = int(table_id) - 1
                table = db.readTable(int(table_id))
                if table:
                    svg_content = table.svg()
                    self.serve_svg_content(svg_content)  # Serve the SVG content directly
                else:
                    self.send_error(404, 'Game not initialized')
                db.close()
            else:
                self.send_error(400, 'Table ID not specified')
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/initializeGame':
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']})
            player1_name, player2_name = form.getvalue('player1Name'), form.getvalue('player2Name')
            table = initialize_table_with_balls()

            db = Physics.Database(reset=True)
            db.createDB()

            db = Database()
            table_id = db.writeTable(table)
            db.close()
            self.send_response(302)
            self.send_header('Location', f'/game?table_id={table_id}')
            self.end_headers()
        elif parsed_path.path == '/processShot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            shot_data = json.loads(post_data.decode('utf-8'))

            # Convert mouse drag distance to initial velocities
            xvel = shot_data['deltaX'] * 10  # Adjust multiplier as needed
            yvel = shot_data['deltaY'] * 10  # Adjust multiplier as needed

            # Retrieve the latest table state to apply the shot
            latest_table_id = self.db.get_latest_table_id()
            table = self.db.readTable(latest_table_id)

            # Assuming 'Game' class is initialized and accessible as 'self.game'
            self.game.shoot(self.game.gameName, self.game.player1Name, table, xvel, yvel)  # player1Name is an example; determine the player based on your logic

            # Respond to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'message': 'Shot processed successfully'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, 'File Not Found')


    def initialize_game_and_add_players(self, player1_name, player2_name):
        print("Inserting game and players into database")
        # Insert game and players into the database
        self.db_cursor.execute("INSERT INTO Game (GAMENAME) VALUES ('New Pool Game')")
        game_id = self.db_cursor.lastrowid

        self.db_cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player1_name))
        self.db_cursor.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (game_id, player2_name))

        self.db_conn.commit()

        print(f"Game {game_id} initialized with players {player1_name} and {player2_name}")

        # Initialize a new table state
        # Use the shoot method from your Game class in Physics.py as a reference
        table = Physics.Table()
        Physics.Game().shoot('New Pool Game', player1_name, table, 0, 0)  # Modify as needed

        return game_id

    def log_message(self, format, *args):
        return  # Override to disable automatic logging of requests by BaseHTTPServer

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Server listening on port {port}")
    httpd.serve_forever()
