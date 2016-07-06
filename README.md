# evo2016
Reference page for our annual EVO fantasy league. Places MIOM-ranked players in a highly visible section at the top of the site, and displays pool links for all entrants. Intended to be used as a draft selection aid.

Implementation-wise, you shouldn't expect anything particularly interesting. After player data is obtained from EVO's pool pages, the `parse.py` script generates HTML content and outputs it as an arbitrary file. You can try this out yourself if you have nothing better to do.

The below command will scrape player information from EVO's S3-hosted bracket listings. Note that it will probably stop working soon after July 17th, or whenever the official S3 pages go down.
```
./scrape.py players
```

To create the HTML file (**after** `scrape.py` has been run):
```
./parse.py [output_path] # default is ./index.html
```

Equivalently, replace both commands with
```
make # ...or
make custom [output_path]
```
