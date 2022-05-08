package main

import (
	"fmt"
	"knowledgejournal/cli"
	"knowledgejournal/database"
)

func main() {
	fmt.Println("Hello, Modules!")
	cli.PrintHello()
	database.Initialise("my.db")
}
