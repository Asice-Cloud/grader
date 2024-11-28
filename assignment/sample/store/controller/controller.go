package controller

type Controller struct {
	Hello
	Store
}

func New() *Controller {
	Controller := &Controller{}
	return Controller
}
