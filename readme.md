# moviedl

Why torrent your movies and/or series if you can simply get the fastest direct download/stream links?

Similarly, the mechanisms used in this program makes fetching as fast as possible ;).

### Providers

moviedl is provided with its stream by the following websites:

| Website | Working | Quality | Provided Content | 
| ------- | ------- | ------- | ---------------- |
| [WatchSeries](https://swatchseries.ru/) | Yes | Highest Possible | Movie & Series |
| [FBox](https://fbox.to/) | Yes | Highest Possible | Movie & Series |

### Commandline Arguments

Below are the most important command line arguments available in twistdl

| Argument | Alias | Description |
| --- | --- | --- |
| `--search` | `-s` | Search through [WatchSeries](https://swatchseries.ru/). | 
| `--download` | `-dl` | Download content using URL. | 
| `--grab` | `-g` | Grab the stream url of content without downloading. This will also require URL. |
| `--list` | `-l` | Set a list of episodes to download from (if it's a series). Put in '1:1 2:3' arguments to get S1E1 and S2E3. |

Below are, well, commandline flags for available in twistdl.

| Flags (Toggleable arguments) | Alias | Description |
| --- | --- | --- |
| `--iafl`| --- | This activates "I am feeling lucky" mode which is set to download the first result (if the user uses `--search`). Range is applicable here. |
| `--quiet` | `-q` | This basically removes tqdm progress bar shown during downloading. |

### Can't download?

If you can't download, it's possibly because the stream links do not contain a mp4 URL. You can simply use `-g` argument to get the stream link and download it in a external HLS downloader.