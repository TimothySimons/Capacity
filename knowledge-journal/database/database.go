package database

import (
	"log"
	"github.com/boltdb/bolt"
)

type entry struct {
	question string;
}

func Initialise(filepath string) *bolt.DB {
	db, err := bolt.Open(filepath, 0600, nil)
	if err != nil {
		log.Fatal(err)
	}
	return db
}




