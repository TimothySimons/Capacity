// TODO: consider formatting returned errors to aid debugging - https://earthly.dev/blog/golang-errors/#:~:text=Go's%20built%2Din%20errors%20don,surprisingly%20lightweight%20and%20simple%20design.
// TODO: consider refactoring error-handling (maybe some if err != nil checks?)

package datastore

import (
	"encoding/json"
	"fmt"

	"github.com/boltdb/bolt"
)

// Database encapsulates an MCQ knowledgebase.
// The struct abstracts away the bolt database and corresponding bolt operations.
type Database struct {
	bolt_db *bolt.DB
}

type DatabaseEntry struct {
	Question    string
	Options     []string
	Answers     []string
	Explanation string
}

func PrintHello() {
	fmt.Println("Hello, Modules! This is database speaking!")
}

func InitialiseDatabase(filepath string) (Database, error) {
	db, err := bolt.Open(filepath, 0600, nil)
	database := Database{
		bolt_db: db,
	}
	return database, err
}

func (database Database) Close() {
	db := database.bolt_db
	defer db.Close()
}

func (database Database) CreateBucket(bucketName string) error {
	db := database.bolt_db
	err := db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucket([]byte(bucketName))
		return err
	})
	return err
}

func (database Database) AddEntry(bucketName string, entry DatabaseEntry) error {
	db := database.bolt_db
	err := db.Update(func(tx *bolt.Tx) error {
		encodedEntry, err := json.Marshal(entry)
		if err != nil {
			return err
		}

		bucket := tx.Bucket([]byte(bucketName))
		err = bucket.Put([]byte("0"), encodedEntry)
		return err
	})
	return err
}
