from playlist_data import sp

def get_playlist_data(playlist_link):
    '''
    Get metadata + track data from a public Spotify playlist link.
    '''
    tracks = []

    try:
        # get first 100 tracks + metadata
        results = sp.playlist(playlist_id=playlist_link)
        if (results != None and 'tracks' in results):
            tracks.extend(results['tracks']['items'])
        metadata = get_metadata(results)

        # get first set of tracks beyond first 100 tracks, if they exist
        if('next' in results['tracks'] and next != None):
            results = sp.next(results['tracks'])
            if (results != None and 'items' in results):
                tracks.extend(results['items'])

            # get any tracks beyond first 200 tracks, if they exist
            while(results != None and 'next' in results and results['next'] != None):
                results = sp.next(results)
                if (results != None and 'items' in results):
                    tracks.extend(results['items'])
    except:
        return (None, None)
    
    return (metadata, tracks)

def get_metadata(playlist_data):
    '''
    Parse the JSON returned by Spotify API's "Get Playlist" endpoint to get
    useful metadata.
    '''
    parsed_data = {}
    parsed_data["playlist_title"] = playlist_data["name"]
    parsed_data["playlist_owner"] = playlist_data["owner"]["display_name"]
    parsed_data["number_of_tracks"] = playlist_data["tracks"]["total"]
    return parsed_data

def get_attr_data(tracks):
    '''
    Get all of this playlist's tracks' audio features/attributes.
    '''
    attributes = []
    num_tracks = len(tracks)

    # get track audio features 100 at a time
    for i in range(0, num_tracks, 100):
        batch = tracks[i:(min(num_tracks-1, i+100))]
        batch_ids = []
        for track in batch:
            batch_ids.append(track['track']['uri'])
        attributes.extend(sp.audio_features(batch_ids))
    
    return attributes

def get_avg_attr_data(attributes):
    '''
    Get the average of this playlist's audio attribute data.
    '''
    num_tracks = len(attributes)
    valence_sum = 0
    energy_sum = 0
    acousticness_sum = 0
    tempo_sum = 0
    
    for track in attributes:
        valence_sum += track["valence"]
        energy_sum += track["energy"]
        acousticness_sum += track["acousticness"]
        tempo_sum += track["tempo"]
    
    averages = {}
    averages["valence"] = valence_sum / num_tracks
    averages["energy"] = energy_sum / num_tracks
    averages["acousticness"] = acousticness_sum / num_tracks
    averages["tempo"] = tempo_sum / num_tracks

    return averages