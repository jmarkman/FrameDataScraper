# Frame Data Scraper

This cmd line program will return frame data for various characters in Super Smash Brothers Ultimate. Fortunately, there's a singular site that has risen up in terms of aggregating data, but it's a mostly-frontend webpage where the creator enters all values by hand. This will be the program's target for scraping.

Since the creator edits it by hand, I doubt there's frame data history to access.

I'm honestly just toying with the idea of this, because the web scraping is the easy part. The more complicated/interesting part is what to do *after* scraping: it'd be best if the scraping was a one-and-done operation, so this could probably just have a singular purpose of scraping the site and spitting out the results to a sqlite DB, but that would require creating a database schema. That shouldn't be *too* hard.

All documentation is "if I do it" (I tend to do it out of habit anyway), but I'll put most of my technical thoughts and overall planning in PLANNING.md
