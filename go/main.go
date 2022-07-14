// package is a go keyword that is essentially a namespace
// for all things defined within it.
// The package name is abitrary with the expection of main
// which tells the compiler that this is the code entrypoint
package main

// import the following packages.
// All of these are part of Go's standard library
import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

// Here we define some constants of type 'string'
// A constant cannot be changed anywhere in the code
// once delared initially
const (
	APIEndpoint   string = "https://dataservice.accuweather.com"
	APIKey        string = "bTWRzyxjP94K3Wn66NlQsr3h2qppp3cs"
	LocationsPath string = "locations/v1/regions"
)

// Here we create a new data type called Location that is a struct
// A struct is a data object that has named fields of type string
type Location struct {
	EnglishName   string
	ID            string
	LocalizedName string
}

// Here we create a new data type called Locations.
// This is a slice (list, array) of the Location type defined above
type Locations []Location

// getLocation is a function that takes a single argument 'url' if type string.
// it returns something of type Locations and type error
func getLocations(url string) (Locations, error) {
	// Here we create a new variable called locations of type Locations
	var locations Locations

	// Here we call the http package's Get method passing in 'url' as
	// an argument. It return 2 values that we assign to variables
	// 'resp' and 'err'
	resp, err := http.Get(url)
	// if the err variable is not equal to 'nil' then we return locations, and err
	if err != nil {
		return locations, err
	}
	// We need to call the Close() method on the response body after we've
	// finished reading it. But rather that do the close later in the function
	// after we have read it, we can defer the close here. So that it get's
	// called as the function exits
	defer resp.Body.Close()

	// Here we call the io package's ReadAll() function passing in the response body
	// it returns 2 values that we assign to variables body and err.
	// body is a slice of type 'byte' ([]byte)
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return locations, err
	}

	// Here we call the json package's Unmarshal function passing in body
	// which is []byte and the reference to the locations variable
	// if there is no error we will find that locations declared at the
	// beginning of this funtion is now populated with the json data that was
	// the body. This is possible because our Location struct's fields are the same
	// name as those in the json document.
	err = json.Unmarshal(body, &locations)
	if err != nil {
		return locations, err
	}

	// If we've succeeded to get this far through the function we can return
	// the now populated locations variable and nil as the value for error
	return locations, nil
}

// main is ALWAYS the first function called inside the main package
// It is the codes entrypoint
func main() {
	locations, err := getLocations(
		// here we use fmt's Sprintf function to format a string. In our case
		// the url that we need to pass into getLocations()
		fmt.Sprintf(
			"%s/%s?apikey=%s",
			APIEndpoint,
			LocationsPath,
			APIKey,
		),
	)
	if err != nil {
		// log's Fatal function is writes to stdout with datetime and the error
		// while also exitting 1
		log.Fatal(err)
	}

	// fmt's Printf function allows is to format strings and write to stdout
	// Here we use the %#v token that will let us inspect the locations variable
	fmt.Printf("%#v\n", locations)

	// Here we range (loop) over each item in the locations variable, which is a
	// slice (list) of type Location.
	// range returns the index of the item and the value. Here we don't care about
	// the index, so we use _ to ignore it. We store the value in location.
	// and for each of them we print to stdout
	for _, location := range locations {
		fmt.Printf("%#v\n", location)
	}
}
