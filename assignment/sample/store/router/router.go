package router

import (
	"store/middleware"

	"github.com/gin-gonic/gin"
)

func InitRouter(r *gin.Engine) {
	r.Use(middleware.Error)
	r.Use(middleware.GinLogger(), middleware.GinRecovery(true))
	apiRouter := r.Group("/api")
	{
		// example
		// begin
		apiRouter.GET("/", ctr.Hello.Hello)
		apiRouter.GET("/time", ctr.Hello.HelloTime)
		// end
	}

	store := apiRouter.Group("/store")
	{
		store.POST("/append", ctr.Store.Append)
	}
	data := r.Group("/data")
	{
		data.GET("/generate", func(c *gin.Context) {
			c.JSON(200, gin.H{
				"message": "Data generated",
			})
		})
	}
}
