# Obsidian Smart Link

Automates the process of skimming through notes to see which new pairs could be linked. Adds a pane that lists notes that are currently un-related by links or tags, but seem to have similar content. Should make it easier to connect ideas and spot insights.

Sample:
<img width="267" alt="image" src="https://user-images.githubusercontent.com/6496202/161357681-58022a66-bbcb-4c9b-b4b0-f9965c3d7463.png">


Uses [Obsidian Lab](https://github.com/cristianvasquez/obsidian-lab-py) and [Obsidian Tools](https://github.com/mfarragher/obsidiantools).

Current strategy uses the Universal Sentence Encoder(https://tfhub.dev/google/universal-sentence-encoder/4) by Google for semantic similarity. Seems to beat out naive TFIDF and GloVe models by anecdotal evidence. Works surprisingly well! More tests to come.

## Setup

1. Install Obsidian Lab plugin
2. Install requirements
3. Run the dev lab server
4. Configure the Lab plugin:
   - Panel UI
   - Blocks Widget Icon
   - Additional trigger when opening file

Starting up might be finicky, might have to quit and reopen Obsidian a few times. The panel will be empty while the script runs - logs can be seen in the dev server.

## Dev

To start up the lab server:

```
m/dev.sh
```
