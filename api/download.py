from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import yt_dlp

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
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'dump_single_json': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                
            video_url = None
            if 'formats' in info_dict and isinstance(info_dict['formats'], list):
                for f in info_dict['formats']:
                    if f.get('ext') == 'mp4' and f.get('url'):
                        video_url = f['url']
                        break

            if video_url:
                self.wfile.write(json.dumps({'videoUrl': video_url}).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({'error': 'No MP4 video URL found for the provided link.'}).encode('utf-8'))

        except Exception as e:
            print(f"Error extracting video URL: {e}")
            self.wfile.write(json.dumps({'error': 'Failed to extract video URL.', 'details': str(e)}).encode('utf-8'))
