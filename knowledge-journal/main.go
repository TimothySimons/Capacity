// TODO: consider putting the main.go class in a cmd folder as is seemingly the convention

package main

import (
	"fmt"
	"knowledgejournal/cli"
	"knowledgejournal/datastore"
)

func main() {
	fmt.Println("Hello, Modules!")
	cli.PrintHello()
	datastore.PrintHello()

	database, _ := datastore.InitialiseDatabase("my.db")
	defer database.Close()

	bucketName := "somebucket"
	database.CreateBucket(bucketName)

	var entry datastore.DatabaseEntry
	entry.Question = "this is a question"
	entry.Options = []string{"a", "b", "c", "d"}
	entry.Answers = []string{"a", "d"}
	entry.Explanation = "this is an explanation"

	database.AddEntry(bucketName, entry)
	database.Head(bucketName, 5)

	bucketName = "someOtherBucket"
	database.CreateBucket(bucketName)
	err := database.AddEntriesFromCSV(bucketName, "operating_systems.csv")
	fmt.Println(err)
	err = database.AddEntry(bucketName, entry)
	fmt.Println(err)
	database.Head(bucketName, 10)
}
