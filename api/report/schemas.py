from importlib.metadata import metadata
from apiflask import Schema
from apiflask.fields import Date, Integer


class ReportQueryDaySchema(Schema):
    date = Date(
        required=True,
        metadata={"description": "A report will be generated for the selected date"},
    )


class ReportQueryMonthSchema(Schema):
    month = Integer(
        required=True,
        metadata={"description": "A report will be generated for the selected month"},
    )
    year = Integer(
        required=True, metadata={"description": "The year for the selected month"}
    )


class ReportQueryRangeSchema(Schema):
    start_date = Date(
        required=True,
        metadata={
            "description": "A report will be generated for a range with the selected start date"
        },
    )
    end_date = Date(
        required=True,
        metadata={
            "description": "A report will be generated for a range with the selected end date"
        },
    )


class ReportQueryYearSchema(Schema):
    year = Integer(
        required=True,
        metadata={"description": "A report will be generated for the selected year"},
    )
