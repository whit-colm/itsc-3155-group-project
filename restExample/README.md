# Example REST API implementation

This example API is not an implimentation of the AH API itself, but is meant to show "what" a RESTful API should resemble and how one interacts with it.

The project is a simplified implementation of [Tutorial: Developing a RESTful API with Go and Gin](https://go.dev/doc/tutorial/web-service-gin). I wrote it in Go as this is a language I'm far more comfortable in and is suited towards these kinds of services. I will attempt to document any obvious language ideosyncricies but it shouldn't be to difficult to parse for anyone with a familiarity with a couple other languages.

# Interfacing with the API

In a REST API, a program listens at specific website paths for HTTP requests and then sends a structured data format.

Looking at the `main.go`, everything the program *listens* for is in the `main()` function. i.e. there it shows the webserver is run on `localhost:8080` and listens at `/albums` for the GET and POST HTTP request. The function `getAlbums` and `postAlbums` show what should happen when these request are recieved. Below will show how these are interfaced with.

## GET `/albums`

There is a GET handler at `/albums`. When this is recieved, it lists the albums currently available in JSON.

This can be viewed in browser by navigating to `localhost:8080/albums`, as using a browser implicitly sends a GET method.

You can also use the `curl` command on a bash-like terminal (e.g. the terminals on Linux or macOS, or WSL2 for windows)

```bash
# things in hashes are comments. this can be directly copied and pasted.
curl http://localhost:8080/albums `# curl transfers data from a url` \
    --include `# shows additional information like headers and status` \
    --request "GET" `# The request type, not necessary but helpful to review`
```

## POST `/albums`

There is a POST handler at `/albums`. When this is recieved with some album JSON, it adds the album to the list (which you can see by GETting the albums afterwards). If it succeeds, it send a 200 (success) with the JSON of the album added, otherwise it sends a 400 (Bad Request) and the album which was not added.

This cannot (easily) be done in browser. Use the `curl` command:

```bash
curl http://localhost:8080/albums \
    --include `# show response code and other info` \
    --header "Content-Type: application/json" `# Content-Type tells the server what the data "is"` \
    --request "POST" `# the request type, must be POST to match the handler` \
    --data '{"id": "4","title": "The Modern Sound of Betty Carter","artist": "Betty Carter","price": 49.99}'
            # ^^^ a JSON struct of the album to be added.
```

For a bonus exercise, this data is malformed and will result in an error code.

```bash
curl http://localhost:8080/albums \
    --include `# show response code and other info` \
    --header "Content-Type: application/json" `# Content-Type tells the server what the data "is"` \
    --request "POST" `# the request type, must be POST to match the handler` \
    --data '{' # junk data
```

## GET `/albums/:id`

There is a GET handler at `/albums/:id`. `:id` in this case is a parameter mapped to the ID of an album. It returns either a status code 200 with the JSON representing an album with the id of `:id` (e.g. 1, 2, 3, ...) or a status code 404 if no such album with that ID exists. 

This can be viewed in browser by navigating to `localhost:8080/albums`. 

You can also use the `curl` command

```bash
# an album with ID 1 is guarenteed to exist, see the albums slice on
# line 18 of main.go
curl http://localhost:8080/albums/1 \
    --include \
    --request "GET"
```

```bash
# Try GETting an album with an ID that does not exist, then adding one
# via POST.
curl http://localhost:8080/albums/? \
    --include \
    --request "GET"
```