import time
from typing import Union

from drinks.application.dtos import (
    AddDrinkReviewInputDto,
    AddDrinkReviewOutputDto,
    AddDrinkWishInputDto,
    AddDrinkWishOutputDto,
    CreateDrinkInputDto,
    CreateDrinkOutputDto,
    DeleteDrinkInputDto,
    DeleteDrinkOutputDto,
    DeleteDrinkReviewInputDto,
    DeleteDrinkReviewOutputDto,
    DeleteDrinkWishInputDto,
    DeleteDrinkWishOutputDto,
    FindDrinkInputDto,
    FindDrinkOutputDto,
    FindDrinksInputDto,
    FindDrinksOutputDto,
    UpdateDrinkInputDto,
    UpdateDrinkOutputDto,
    UpdateDrinkReviewInputDto,
    UpdateDrinkReviewOutputDto,
)
from drinks.domain.entities import Drink
from drinks.domain.repository import DrinkRepository
from drinks.domain.value_objects import DrinkRating, DrinkType
from shared_kernel.application.dtos import FailedOutputDto
from shared_kernel.domain.exceptions import ResourceNotFoundError, ResourceAlreadyExistError
from shared_kernel.domain.value_objects import DrinkId


class DrinkApplicationService:
    def __init__(self, drink_repository: DrinkRepository) -> None:
        self._drink_repository = drink_repository

    def find_drink(self, input_dto: FindDrinkInputDto) -> Union[FindDrinkOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(drink_id=DrinkId.from_str(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )

            return FindDrinkOutputDto(
                drink_id=str(drink.id),
                drink_name=drink.name,
                drink_image_url=drink.image_url,
                drink_type=drink.type.value,
                avg_rating=float(drink.avg_rating),
                num_of_reviews=drink.num_of_reviews,
                num_of_wish=drink.num_of_wish,
            )

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def find_drinks(self, input_dto: FindDrinksInputDto) -> Union[FindDrinksOutputDto, FailedOutputDto]:
        try:
            drinks = self._drink_repository.find_all(input_dto.query_param)

            return FindDrinksOutputDto(
                items=[
                    FindDrinksOutputDto.Item(
                        drink_id=str(drink.id),
                        drink_name=drink.name,
                        drink_image_url=drink.image_url,
                        drink_type=drink.type.value,
                        avg_rating=float(drink.avg_rating),
                        num_of_reviews=drink.num_of_reviews,
                        num_of_wish=drink.num_of_wish,
                    )
                    for drink in drinks
                ]
            )

        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def create_drink(self, input_dto: CreateDrinkInputDto) -> Union[CreateDrinkOutputDto, FailedOutputDto]:
        try:
            drink = Drink(
                id=DrinkId.build(drink_name=input_dto.drink_name, created_at=time.time()),
                name=input_dto.drink_name,
                image_url=input_dto.drink_image_url,
                type=DrinkType.from_str(input_dto.drink_type),
            )

            self._drink_repository.add(drink)

            return CreateDrinkOutputDto()

        except ResourceAlreadyExistError as e:
            return FailedOutputDto.build_resource_conflict_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_drink(self, input_dto: UpdateDrinkInputDto) -> Union[UpdateDrinkOutputDto, FailedOutputDto]:
        try:
            drink_id = DrinkId.from_str(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_not_found_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

            drink = Drink(
                id=drink_id,
                name=input_dto.drink_name,
                image_url=input_dto.drink_image_url,
                type=input_dto.drink_type,
                avg_rating=DrinkRating(value=input_dto.avg_rating),
                num_of_reviews=input_dto.num_of_reviews,
                num_of_wish=input_dto.num_of_wish,
            )
            self._drink_repository.update(drink)

            return UpdateDrinkOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink(self, input_dto: DeleteDrinkInputDto) -> Union[DeleteDrinkOutputDto, FailedOutputDto]:
        try:
            drink_id = DrinkId.from_str(input_dto.drink_id)
            if self._drink_repository.find_by_drink_id(drink_id) is None:
                return FailedOutputDto.build_resource_not_found_error(f"{str(drink_id)}의 술을 찾을 수 없습니다.")

            self._drink_repository.delete_by_drink_id(drink_id)

            return DeleteDrinkOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def add_drink_review(self, input_dto: AddDrinkReviewInputDto) -> Union[AddDrinkReviewOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(DrinkId.from_str(input_dto.drink_id))

            drink.add_rating(input_dto.drink_rating)
            self._drink_repository.update(drink)

            return AddDrinkReviewOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def update_drink_review(
        self, input_dto: UpdateDrinkReviewInputDto
    ) -> Union[UpdateDrinkReviewOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(DrinkId.from_str(input_dto.drink_id))
            if drink is None:
                return FailedOutputDto.build_resource_not_found_error(
                    message=f"{str(input_dto.drink_id)}의 술을 찾을 수 없습니다."
                )

            drink.update_rating(
                old_rating=input_dto.old_drink_rating,
                new_rating=input_dto.new_drink_rating,
            )
            self._drink_repository.update(drink)

            return UpdateDrinkReviewOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink_review(
        self, input_dto: DeleteDrinkReviewInputDto
    ) -> Union[DeleteDrinkReviewOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(DrinkId.from_str(input_dto.drink_id))

            drink.delete_rating(input_dto.drink_rating)
            self._drink_repository.update(drink)

            return DeleteDrinkReviewOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def add_drink_wish(self, input_dto: AddDrinkWishInputDto) -> Union[AddDrinkWishOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(DrinkId.from_str(input_dto.drink_id))

            drink.add_wish()
            self._drink_repository.update(drink)

            return AddDrinkWishOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))

    def delete_drink_wish(
        self, input_dto: DeleteDrinkWishInputDto
    ) -> Union[DeleteDrinkWishOutputDto, FailedOutputDto]:
        try:
            drink = self._drink_repository.find_by_drink_id(DrinkId.from_str(input_dto.drink_id))

            drink.delete_wish()
            self._drink_repository.update(drink)

            return DeleteDrinkWishOutputDto()

        except ResourceNotFoundError as e:
            return FailedOutputDto.build_resource_not_found_error(message=str(e))
        except Exception as e:
            return FailedOutputDto.build_system_error(message=str(e))
