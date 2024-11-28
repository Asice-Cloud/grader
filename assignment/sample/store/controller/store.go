package controller

import (
	"github.com/gin-gonic/gin"
	"store/model"
)

type Store struct {
}

func (s *Store) Append(c *gin.Context) {
	var food model.Food
	err := c.ShouldBindJSON(&food)
	if err != nil {
		c.JSON(400, gin.H{"msg": err.Error()})
		return
	}
	code, err := srv.Store.Append(food)
	if err != nil {
		c.JSON(500, gin.H{"msg": err.Error()})
		return
	}
	switch code {
	case 0:
		c.JSON(200, gin.H{"msg": "existed"})
	case -1:
		c.JSON(500, gin.H{"msg": "failed"})
	case 1:
		c.JSON(201, gin.H{"msg": "created"})
	}
}
