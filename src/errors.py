from typing import Any, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class BbsException(Exception):
    """Base class for all BBS errors"""
    pass


class InvalidToken(BbsException):
    """User has provided an invalid or expired token"""
    pass


class RevokedToken(BbsException):
    """User has provided a token that has been revoked"""
    pass


class AccessTokenRequired(BbsException):
    """User has provided a refresh token when an access token is needed"""
    pass


class RefreshTokenRequired(BbsException):
    """User has provided an access token when a refresh token is needed"""
    pass


class UserAlreadyExists(BbsException):
    """User with this email already exists"""
    pass


class InvalidCredentials(BbsException):
    """Wrong email or password"""
    pass


class UserNotFound(BbsException):
    """User not found"""
    pass


class BarbershopNotFound(BbsException):
    """Barbershop not found"""
    pass


class ServiceNotFound(BbsException):
    """Service not found"""
    pass


class ScheduleNotFound(BbsException):
    """Schedule not found"""
    pass


class BookingNotFound(BbsException):
    """Booking not found"""
    pass


class ReviewNotFound(BbsException):
    """Review not found"""
    pass


class PaymentNotFound(BbsException):
    """Payment not found"""
    pass


class InsufficientPermission(BbsException):
    """User does not have the necessary permissions"""
    pass


class BookingConflict(BbsException):
    """Booking conflict (e.g., slot already booked)"""
    pass


class DuplicateReview(BbsException):
    """Review for this booking already exists"""
    pass


class DuplicatePayment(BbsException):
    """Payment for this booking already exists"""
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BbsException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(403, {"message": "Token is invalid or expired", "error_code": "invalid_token"}),
    )
    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(403, {"message": "Token has been revoked", "error_code": "revoked_token"}),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(403, {"message": "Please provide an access token", "error_code": "access_token_required"}),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(403, {"message": "Please provide a refresh token", "error_code": "refresh_token_required"}),
    )
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(403, {"message": "User with this email already exists", "error_code": "user_exists"}),
    )
    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(403, {"message": "Invalid email or password", "error_code": "invalid_credentials"}),
    )
    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(404, {"message": "User not found", "error_code": "user_not_found"}),
    )
    app.add_exception_handler(
        BarbershopNotFound,
        create_exception_handler(404, {"message": "Barbershop not found", "error_code": "barbershop_not_found"}),
    )
    app.add_exception_handler(
        ServiceNotFound,
        create_exception_handler(404, {"message": "Service not found", "error_code": "service_not_found"}),
    )
    app.add_exception_handler(
        ScheduleNotFound,
        create_exception_handler(404, {"message": "Schedule not found", "error_code": "schedule_not_found"}),
    )
    app.add_exception_handler(
        BookingNotFound,
        create_exception_handler(404, {"message": "Booking not found", "error_code": "booking_not_found"}),
    )
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(404, {"message": "Review not found", "error_code": "review_not_found"}),
    )
    app.add_exception_handler(
        PaymentNotFound,
        create_exception_handler(404, {"message": "Payment not found", "error_code": "payment_not_found"}),
    )
    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(403, {"message": "You are not allowed to perform this action", "error_code": "insufficient_permission"}),
    )
    app.add_exception_handler(
        BookingConflict,
        create_exception_handler(400, {"message": "Booking conflict", "error_code": "booking_conflict"}),
    )
    app.add_exception_handler(
        DuplicateReview,
        create_exception_handler(400, {"message": "Review for this booking already exists", "error_code": "duplicate_review"}),
    )
    app.add_exception_handler(
        DuplicatePayment,
        create_exception_handler(400, {"message": "Payment for this booking already exists", "error_code": "duplicate_payment"}),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={"message": "Oops! Something went wrong", "error_code": "internal_error"},
            status_code=500,
        )
