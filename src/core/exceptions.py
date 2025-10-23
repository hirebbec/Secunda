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


class ModelEncodeValidationError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)
