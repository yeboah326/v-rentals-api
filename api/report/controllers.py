from urllib import response
from apiflask import APIBlueprint, input, output, doc, HTTPError
from flask_jwt_extended import jwt_required
from api.extensions import limiter
from .schemas import *


report = APIBlueprint("report", __name__, url_prefix="/api/report")


@report.post("/day")
@input(ReportQueryDaySchema)
@doc(
    summary="Generate summary for day",
    description="An endpoint to generate a report for a given date",
    responses=[200, 401],
)
@limiter.limit("1/minute")
@jwt_required()
def report_generate_day():
    pass


@report.post("/range")
@input(ReportQueryRangeSchema)
@doc(
    summary="Generate a report for range",
    description="An endpoint to generate a report for a given range of dates",
    responses=[200, 401],
)
@limiter.limit("1/minute")
@jwt_required()
def report_generate_range():
    pass


@report.post("/month")
@input(ReportQueryMonthSchema)
@doc(summary="Generate a report for a given month"
, description="An endpoint to generate a report for a given month and year",
responses=[200, 401]
)
@limiter.limit("1/minute")
@jwt_required()
def report_generate_month():
    pass


@report.post("/year")
@input(ReportQueryYearSchema)
@doc(summary="Generate a report for a given year",
description="An endpoint to generate a report for a given year",
responses=[200, 401]
)
@limiter.limit("1/minute")
@jwt_required()
def report_generate_year():
    pass
