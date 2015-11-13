==================
soundcloud-streams
==================

An implementation of user-curated streams, based on a given list of SoundCloud users, in the form of playlists.

## Motivation

One feature I find lacking in SoundCloud is the ability to filter my stream based on what I want to listen to. For example, at times I want only to listen to my favorite artists, while at other times, I want to look specifically at users with relatively low follower counts, or blogs. The list goes on - certain genres, playlists, track durations, BPMs, user locations, etc are all factors that can help filter the stream down to what I really want. SoundCloud has nothing to show for this, so I decided to create it.

## Usage

The script requires the following to run:

* SoundCloud OAuth2 credentials ([register an app](http://soundcloud.com/you/apps/) if you have not yet done so)
* A set of parameters to filter by, given in JSON format

To create (or update) a stream, simply fill out the `inputs.py` file with the above, and set the given variables to your liking:

| Variable | Type | Purpose |
| --- | --- | --- |
| `new` | Boolean | `True`: Create new stream<br />`False`: Update existing stream |
| `goto` | Boolean | Determines whether stream will be opened in browser upon completion |
| `title` | String | If creating a new stream, provide the desired title here |
| `permalink` | String | If updating an existing stream, identify it by its permalink (i.e. soundcloud.com/you/sets/THIS) here |
| `public` | Boolean | Choose whether stream will be made public |

Then, run `streams.py` to create/update your stream. Due to limitations on SoundCloud playlists, streams are truncated to 200 tracks.

## Example

Adhere to the following formatting when providing a JSON file as your parameters:

```
{
  "users": [
    "feedme",
    "fuckmylife",
    "prettylights",
    "dillonfrancis",
    "chrome-sparks",
    "spor",
    "flume",
    "gramatik",
    "koan-sound",
    "nero",
    "rudebrat",
    "seamlessr",
    "seven-lions",
    "xilent"
  ],
  "filters": {
    "duration": {
      "from": 15000,
      "to": 900000
    }
  }
}
```

These parameters result in a [stream](https://www.soundcloud.com/srsbusiness/sets/favorite-artists) of some of my favorite artists.

The `filters` object is optional, as this was used in the example to filter out tracks pertaining to samples/clips (<15 sec) and mixes/podcasts (>15 min).

## To Do

- [ ] Implement UI for parameter specification
- [ ] Support use of txt file as parameters
- [ ] Generalize search options to include
  - [ ] Genre
  - [ ] BPM
  - [ ] User properties (location, track count, etc)
  - [ ] A user's favorites & reposts
  - [ ] Playlists
  - [ ] Podcasts & Mixes
- [ ] Set playlist image as stream title or custom art
- [ ] Add options for union/intersection of multiple parameter files

## History

### 0.1 // 2015-11-12
Initial release

## Credits

soundcloud-streams was written by [Steven Salka](https://www.linkedin.com/in/ssalka).

## License

soundcloud-streams is published under a [BSD License](https://www.github.com/ssalka/soundcloud-streams/LICENSE).