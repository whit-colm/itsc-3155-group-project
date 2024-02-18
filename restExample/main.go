package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// album represents data about a record album.
type album struct {
	ID     string  `json:"id"`
	Title  string  `json:"title"`
	Artist string  `json:"artist"`
	Price  float64 `json:"price"`
}

// albums slice to seed record album data.
var albums = []album{
	{ID: "1", Title: "Blue Train", Artist: "John Coltrane", Price: 56.99},
	{ID: "2", Title: "Jeru", Artist: "Gerry Mulligan", Price: 17.99},
	{ID: "3", Title: "Sarah Vaughan and Clifford Brown", Artist: "Sarah Vaughan", Price: 39.99},
}

// getAlbums responds with the list of all albums as JSON.
//
// gin.Context is the most important part of Gin. It carries request details,
// validates and serializes JSON, and more.
// https://pkg.go.dev/github.com/gin-gonic/gin#Context
func getAlbums(c *gin.Context) {
	// IndentedJSON serializes `albums` into (pretty) JSON. We also
	// send http.StatusOK (200)
	//      ^^^^           ^^^
	//      Go HTTP pkg    HTTP code 200 is "OK"
	//
	// https://pkg.go.dev/github.com/gin-gonic/gin#Context.IndentedJSON
	c.IndentedJSON(http.StatusOK, albums)
}

// postAlbums adds an album from JSON received in the request body.
func postAlbums(c *gin.Context) {
	var newAlbum album

	// Call BindJSON to bind the received JSON to
	// newAlbum.
	if err := c.BindJSON(&newAlbum); err != nil {
		// if there's an error from the binding, send a 401.
		c.IndentedJSON(http.StatusBadRequest, newAlbum)
		return
	}

	// Add the new album to the slice.
	albums = append(albums, newAlbum)
	// send a 201 that the thing worked.
	c.IndentedJSON(http.StatusCreated, newAlbum)
}

// getAlbumByID locates the album whose ID value matches the id
// parameter sent by the client, then returns that album as a response.
func getAlbumByID(c *gin.Context) {
	// the :id in main gets processed here
	// https://pkg.go.dev/github.com/gin-gonic/gin#Context.Param
	id := c.Param("id")

	// Loop over the list of albums, looking for
	// an album whose ID value matches the parameter.
	for _, a := range albums {
		if a.ID == id {
			c.IndentedJSON(http.StatusOK, a)
			return
		}
	}
	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "album not found"})
}

func main() {
	// Gets a "default" gin.Engine, with some default kit attached
	// like a logger and recovery. Don't worry about this.
	router := gin.Default()
	// HTTP GET requests to /albums will receive the json from getAlbums
	router.GET("/albums", getAlbums)
	// HTTP GET requests to /albums/:id will receive the album with id ":id" (1, 2, 3, ...)
	router.GET("/albums/:id", getAlbumByID)
	router.POST("/albums", postAlbums)

	// Run the thing at localhost:8080
	router.Run("localhost:8080")
}
