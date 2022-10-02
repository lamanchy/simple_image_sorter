# simple image sorter
by Ondřej Lomič

## Thoughts
- My first though was: No way I'm gonna spend week on this, let's do it in one day! :D
- I've used Kafka in the past, but I'll use Nats, since it's your preference. 
(shouldn't be too different).
- I'll use Flask for web interface, I've learned it two days ago and it seems like
a good fit.
- I'll keep it as simple as possible, when not being sure I'll choose the simpler
way. 

## Design
- Reader module watches for changes in the `images/source` folder, but it looks at
the modified time, so new images have to be created, not copied. It uploads the whole
content on startup (configurable) and you can easily force re-upload by re-saving the
image. (There could be better solution to this, but... this is simple and it works)

## Implementation
- I would split config (file paths, logging config) and implementation into multiple
files, but I kept it in one for convenience (it's not really huge project)
- I've used pydantic for validation, I'm used to DRF which is prettier I guess, but
that has Django as dependency, so... Pydantic was a better choice (and it's not that 
different)
- Modules should exit gracefully on first CTRL+C, and they don't, and I don't care 
enough :D. I hope that's alright ;)

## Deployment
- `make` builds Docker images
- `make run` runs pipeline
- `make interface` runs web interface on `localhost:5000`
- `make test` runs... tests :)
- But you can run `docker-compose` directly, just see `Makefile`

## Testing
- I wrote unit tests only for color processor, they didn't make sense to me in other 
places.
- For real project I would write end-to-end tests, that would (IMHO) suit this project
much better. So I wrote them, for valid and invalid file.
- Real end-to-end test would run on a different folders, it is nice to have testing
images named like `__valid_test_image.png`, but not enough. It would be easy to do 
so, just overwrite the mounted volumes in `docker-compose/test.yaml` for each service, 
but.. I would say that's not scope of this demo project.

There's more that could be improved, but there always is. And... I've spent the 
one day to finish the task, so... It has to be finished. :D

Thanks, have a nice day ;)