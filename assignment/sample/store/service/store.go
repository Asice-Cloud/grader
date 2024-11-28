package service

import (
	"gorm.io/gorm"
	"store/model"
)

type Store struct {
}

func (s *Store) Append(food model.Food) (int, error) {
	var exist model.Food
	result := model.DB.First(&exist, "id=?", food.ID)
	if result.Error != nil {
		if result.Error == gorm.ErrRecordNotFound {
			result = model.DB.Create(&food)
			if result.Error != nil {
				return -1, result.Error
			}
			return 1, nil
		}
		return -1, result.Error
	}
	exist.Left += food.Left
	result = model.DB.Save(&exist)
	if result.Error != nil {
		return -1, result.Error
	}
	return 0, nil
}
