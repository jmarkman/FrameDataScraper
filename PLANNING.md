# Experimental Planning

The URL to the frame data page is `https://ultimateframedata.com/`

The character names in the url are lower case, and any character that has their name as multiple parts (i.e., Donkey Kong, Rosalina and Luma) would be rendered with an underscore. That means the examples of Donkey Kong and Rosalina and Luma would be:

`donkey_kong`
`rosalina_and_luma`

A decent naive approach would probably be to have some kind of `CharacterScrapeEngine` that can be called for each current character in ultimate and would return a `Character` object, containing the character name and several child classes as properties. Each child class would be a different section of the character attributes (i.e., their normals, specials, etc.)

After the data is aggregated, then what? It's just sitting there in memory. It'd be a huge waste to scrape even *one* character every time just to report on one move. I'd probably need to create a database for the exported results.