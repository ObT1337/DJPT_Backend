
ALTER TABLE playlists ADD COLUMN playlist_name INTEGER
ALTER TABLE playlists ADD COLUMN playlist_nameOrder INTEGER
ALTER TABLE playlists ADD FOREIGN KEY (playlist_name) REFERENCES tracks (id)