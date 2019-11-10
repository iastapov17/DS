package main

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	_ "github.com/lib/pq"
)

type Activity struct {
	AType     string `xml:"type,attr"`
	Code      string `xml:"Code"`
	Date      string `xml:"Date"`
	Departure string `xml:"Departure"`
	Arrival   string `xml:"Arrival"`
	Fare      string `xml:"Fare"`
}

type Activities struct {
	AType string     `xml:"type,attr"`
	A     []Activity `xml:"activity"`
}

type Card struct {
	Number        string       `xml:"number,attr"`
	Bonusprogramm string       `xml:"bonusprogramm"`
	Activities    []Activities `xml:"activities"`
}

type Cards struct {
	CType string `xml:"type,attr"`
	Cards []Card `xml:"card"`
}

type Name struct {
	First string `xml:"first,attr"`
	Last  string `xml:"last,attr"`
}

type User struct {
	UID string `xml:"uid,attr"`
	N   Name   `xml:"name"`
	C   Cards  `xml:"cards"`
}

type Users struct {
	Version               string `xml:"version,attr"`
	PointzAggregatorUsers []User `xml:"user"`
}

func main() {
	xmlFile, err := os.Open("PointzAggregator-AirlinesData.xml")
	if err != nil {
		fmt.Printf("open file error: %s", err)
		return
	}
	defer xmlFile.Close()
	bv, _ := ioutil.ReadAll(xmlFile)
	var us Users
	err = xml.Unmarshal(bv, &us)
	if err != nil {
		fmt.Println(err)
	}
	servConn := fmt.Sprintf(
		"postgresql://%s:%s@%s:%s%s",
		"denis",
		"denis",
		"94.250.250.51",
		"5432",
		"/ds")

	dbconn, err := sql.Open("postgres", servConn)
	for _, user := range us.PointzAggregatorUsers {
		uid, _ := strconv.Atoi(user.UID)
		// fmt.Printf("%d %s %s\n", uid, user.N.First, user.N.Last)
		name, last := prepare(user.N.First), prepare(user.N.Last)
		if _, err := dbconn.Exec("INSERT INTO userr(usid, fname, lname) VALUES ($1, $2, $3)", uid, name, last); err != nil {
			fmt.Println(err)
		}

		go func(C []Card, uid int, ctype string) {
			for _, card := range C {
				// fmt.Printf("%s %s %s %s\n", card.Number, user.UID, user.C.CType, card.Bonusprogramm)
				if _, err := dbconn.Exec("INSERT INTO card(num, usid, ctype, bonusprogramm) VALUES ($1, $2, $3, $4)", card.Number, uid, ctype, card.Bonusprogramm); err != nil {
					fmt.Println(err)
				}
				for _, activities := range card.Activities {
					go func(one, two string, A []Activity) {
						for _, activity := range A {
							// fmt.Printf("%s %s %s %s %s %s %s %s\n", card.Number, activities.AType, activity.AType, activity.Code, activity.Date, activity.Departure, activity.Arrival, activity.Fare)
							if _, err := dbconn.Exec("INSERT INTO activity(num, astype, atype, code, datee, departure, arrival, fare) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)", one, two, activity.AType, activity.Code, activity.Date, activity.Departure, activity.Arrival, activity.Fare); err != nil {
								fmt.Println(err)
							}
						}
					}(card.Number, activities.AType, activities.A)
				}
			}
		}(user.C.Cards, uid, user.C.CType)
	}
}

var repl = map[string]string{
	"YA":   "IA",
	"YU":   "IU",
	"EY":   "EI",
	"IY":   "II",
	"'Y":   "I",
	"'":    "",
	"SHCH": "SH",
	"TC":   "TS",
}

func prepare(s string) string {
	for i := range repl {
		s = strings.Replace(s, i, repl[i], -1)
	}
	return s
}
