package service

type Service struct {
	Hello
	Store
}

func New() *Service {
	service := &Service{}
	return service
}
