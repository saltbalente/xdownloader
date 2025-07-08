const { YouTubeDl } = require('youtube-dl-exec');

module.exports = async (req, res) => {
    const { url } = req.query;

    if (!url) {
        return res.status(400).json({ error: 'URL parameter is required.' });
    }

    try {
        const ytDlp = new YouTubeDl();
        const info = await ytDlp.exec(url, {
            dumpSingleJson: true,
            noCheckCertificates: true,
            noWarnings: true,
            format: 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        });

        // Find the best quality MP4 video URL
        let videoUrl = null;
        if (info.formats && Array.isArray(info.formats)) {
            for (const format of info.formats) {
                if (format.ext === 'mp4' && format.url) {
                    videoUrl = format.url;
                    break; // Take the first MP4 format found
                }
            }
        }

        if (videoUrl) {
            res.status(200).json({ videoUrl });
        } else {
            res.status(404).json({ error: 'No MP4 video URL found for the provided link.' });
        }

    } catch (error) {
        console.error('Error extracting video URL:', error);
        res.status(500).json({ error: 'Failed to extract video URL.', details: error.message });
    }
};
