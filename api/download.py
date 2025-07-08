from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import subprocess
import sys

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        query = {}
        if '''?''' in s:
            query = parse_qs(urlparse(s).query)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        url = query.get('url', [None])[0]

        if not url:
            self.wfile.write(json.dumps({'error': 'URL parameter is required.'}).encode('utf-8'))
            return

        try:
            # Ejecutar yt-dlp con la opción --get-url para obtener la URL directa del video
            # sys.executable -m yt_dlp asegura que se use el yt-dlp instalado en el entorno de Vercel
            command = [sys.executable, '-m', 'yt_dlp', '--get-url', url]
            
            # Usar subprocess.run para capturar la salida estándar
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            video_url = result.stdout.strip()

            if video_url:
                self.wfile.write(json.dumps({'videoUrl': video_url}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({'error': 'No video URL found for the provided link.'}).encode('utf-8'))

        except subprocess.CalledProcessError as e:
            # Capturar errores específicos de yt-dlp
            print(f"yt-dlp error: {e.stderr}")
            self.wfile.write(json.dumps({'error': 'Failed to extract video URL from yt-dlp.', 'details': e.stderr}).encode('utf-8'))
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error extracting video URL: {e}")
            self.wfile.write(json.dumps({'error': 'Failed to extract video URL.', 'details': str(e)}).encode('utf-8'))