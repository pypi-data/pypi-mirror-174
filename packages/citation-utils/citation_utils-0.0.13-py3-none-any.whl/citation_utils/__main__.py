import datetime
from enum import Enum
from typing import Iterator

from citation_report import Report
from pydantic import BaseModel, Field
from slugify import slugify

from .constructors import ModelAC, ModelAM, ModelBM, ModelGR, Style


class DocketCategory(str, Enum):
    GR = Style.GR.value.short_category
    AM = Style.AM.value.short_category
    AC = Style.AC.value.short_category
    BM = Style.BM.value.short_category


class Citation(BaseModel):
    """The col and index fields are populated in anticipation of future use via the `sqlpyd` library."""

    docket: str | None = Field(None, col=str, index=True)
    docket_category: DocketCategory | None = Field(None, col=str, index=True)
    docket_serial: str | None = Field(None, col=str, index=True)
    docket_date: datetime.date | None = Field(
        None,
        col=datetime.date,
        index=True,
    )
    phil: str | None = Field(None, col=str, index=True)
    scra: str | None = Field(None, col=str, index=True)
    offg: str | None = Field(None, col=str, index=True)

    class Config:
        use_enum_values = True

    @property
    def has_citation(self):
        els = [self.docket, self.scra, self.phil, self.offg]
        values = [el for el in els if el is not None]
        return values

    @property
    def display(self):
        """Combine citation strings into a descriptive string."""
        if self.has_citation:
            return ", ".join(self.has_citation)
        return "No citation detected."

    @property
    def slug(self) -> str | None:
        """If any of the possible values are present, convert this into a slug that can serve as a primary key."""
        if self.has_citation:
            return slugify(" ".join(self.has_citation)).strip()
        return None

    @classmethod
    def from_details(cls, data: dict):
        """Requires `docket`, `scra`, `phil` and `offg` keys set in the `data` dictionary. This enables creation of the Citation object from the originally scraped details.yaml"""
        cite = None
        if data.get("docket"):
            try:
                cite = next(cls.find_citations(data["docket"]))
            except StopIteration:
                cite = None
        return cls(
            docket=cite.docket if cite else None,
            docket_category=cite.docket_category if cite else None,
            docket_serial=cite.docket_serial if cite else None,
            docket_date=cite.docket_date if cite else None,
            phil=Report.extract_from_dict(data, "phil"),
            scra=Report.extract_from_dict(data, "scra"),
            offg=Report.extract_from_dict(data, "offg"),
        )

    @classmethod
    def extract_docket(cls, obj):
        options = (ModelAC, ModelAM, ModelBM, ModelGR)
        if isinstance(obj, options) and obj.ids:
            return cls(
                docket=str(obj),
                docket_category=DocketCategory(obj.short_category),
                docket_serial=obj.first_id,
                docket_date=obj.docket_date,
                phil=obj.phil,
                scra=obj.scra,
                offg=obj.offg,
            )

    @classmethod
    def extract_report(cls, obj):
        if isinstance(obj, Report):
            return cls(
                docket=None,
                docket_category=None,
                docket_serial=None,
                docket_date=None,
                phil=obj.phil,
                scra=obj.scra,
                offg=obj.offg,
            )

    @classmethod
    def find_citations(cls, raw: str) -> Iterator["Citation"]:
        """Combine `Docket`s (which have `Reports`), and filtered `Report` models, if they exist."""
        from .helpers import filtered_reports

        if dockets := list(Style.extract(raw)):
            if reports := list(Report.extract(raw)):
                if undocketed := filtered_reports(raw, dockets, reports):
                    for docket in dockets:
                        if obj := cls.extract_docket(docket):
                            yield obj
                    for report in undocketed:
                        if obj := cls.extract_report(report):
                            yield obj
                else:
                    for docket in dockets:
                        if obj := cls.extract_docket(docket):
                            yield obj
                    for report in reports:
                        if obj := cls.extract_report(report):
                            yield obj
            else:
                for docket in dockets:
                    if obj := cls.extract_docket(docket):
                        yield obj
        else:
            if reports := list(Report.extract(raw)):
                for report in reports:
                    if obj := cls.extract_report(report):
                        yield obj
