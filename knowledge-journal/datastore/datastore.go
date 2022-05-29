// TODO: consider formatting returned errors to aid debugging - https://earthly.dev/blog/golang-errors/#:~:text=Go's%20built%2Din%20errors%20don,surprisingly%20lightweight%20and%20simple%20design.
// TODO: consider refactoring error-handling (maybe some if err != nil checks?)
// TODO: implement function that allows you to print out the database (or at least the first few entries - like head?)
// TODO: find a pretty way to print entries (Head func)

package datastore

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/boltdb/bolt"
)

// Database encapsulates an MCQ knowledgebase.
// The struct abstracts away the bolt database and corresponding bolt operations.
type Database struct {
	boltDBPath string
	boltDB     *bolt.DB
}

type DatabaseEntry struct {
	Question    string
	Options     []string
	Answers     []string
	Explanation string
}

func InitialiseDatabase(databasePath string) (Database, error) {
	db, err := bolt.Open(databasePath, 0600, nil)
	database := Database{
		boltDBPath: databasePath,
		boltDB:     db,
	}
	return database, err
}

func (database Database) Close() {
	db := database.boltDB
	defer db.Close()
}

func (database Database) CreateBucket(bucketName string) error {
	db := database.boltDB
	err := db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucket([]byte(bucketName))
		return fmt.Errorf("failed to create bucket %s in database %s: %s", bucketName, database.boltDBPath, err)
	})
	return fmt.Errorf("failed to update database %s: %s", database.boltDBPath, err)
}

func (database Database) AddEntry(bucketName string, entry DatabaseEntry) error {
	db := database.boltDB
	err := db.Update(func(tx *bolt.Tx) error {
		encodedEntry, err := json.Marshal(entry)
		if err != nil {
			return err
		}

		bucket := tx.Bucket([]byte(bucketName))
		err = bucket.Put([]byte("0"), encodedEntry) // TODO: find a better key
		return err
	})
	return err
}

func (database Database) AddEntriesFromCSV(bucketName string, csvPath string) error {
	// TODO: do we want to impose strict requirements on the system
	csvFile, err := os.Open(csvPath)
	if err != nil {
		return err
	}
	defer csvFile.Close()

	csvLines, err := csv.NewReader(csvFile).ReadAll()
	if err != nil {
		return err
	}

	for _, line := range csvLines {
		question := line[0]
		options := strings.Split(line[1], ",") // TODO: is this best practice? surley there is a cleaner way of loading a csv
		answers := strings.Split(line[2], ",")
		explanation := ""

		entry := DatabaseEntry{
			Question:    question,
			Options:     options,
			Answers:     answers,
			Explanation: explanation,
		}
		fmt.Printf("%+v\n\n", entry)
		database.AddEntry(bucketName, entry)
	}
	return nil
}

func (database Database) Head(bucketName string, n int) error {
	db := database.boltDB
	err := db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(bucketName))
		cursor := bucket.Cursor()

		index := 0
		for key, value := cursor.First(); key != nil && index != n; key, value = cursor.Next() {
			var entry DatabaseEntry
			err := json.Unmarshal(value, &entry)
			if err != nil {
				return err
			}
			index += 1
		}
		return nil
	})
	return err
}
