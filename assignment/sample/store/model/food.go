package model

type Food struct {
	ID           uint   `json:"id" gorm:"primary_key"`
	Name         string `json:"name"`
	Left         int    `json:"left"`
	Produce_date string `json:"produce_date"`
	Expire_date  string `json:"expire_date"`
}
