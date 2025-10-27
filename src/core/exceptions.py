from fastapi import HTTPException, status

organization_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Organization not found",
)

building_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Building not found",
)

activity_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Activity not found",
)

duplicated_activity_name_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Duplicated activity name",
)

duplicated_building_address_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Duplicated building address",
)

duplicated_organization_name_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Duplicated organization name",
)

max_activity_depth_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Maximum activity nesting depth exceeded",
)

building_with_organization_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Try to delete building with organization",
)


class ModelEncodeValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
