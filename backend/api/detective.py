from typing import List

from fastapi import APIRouter

from models.schemas import DataLayer, DetectiveCase, DetectiveQuestion

router = APIRouter()

CASES: List[DetectiveCase] = [
    DetectiveCase(
        id="arctic-vs-antarctic",
        title="The Polar Paradox: Arctic Melting, Antarctic Growing?",
        layer=DataLayer.SEA_ICE,
        regions=["arctic", "antarctic"],
        narrative=(
            "Both poles are warming, yet Arctic sea ice has declined dramatically "
            "while Antarctic sea ice held roughly steady, or even grew slightly, "
            "until around 2014. The same global driver produces opposite regional outcomes."
        ),
        explanation=(
            "The Arctic is an ocean basin surrounded by land, so warming directly "
            "melts sea ice with little else to counteract it. The Antarctic is a "
            "continent surrounded by open ocean; stronger circumpolar winds "
            "(linked to the ozone hole and tropical warming) pushed ice outward, "
            "temporarily offsetting melt, until the trend reversed sharply after 2014."
        ),
        key_mechanism=(
            "Geographic asymmetry: Arctic = ocean basin (direct melt) vs. "
            "Antarctic = continental ice sheet (wind-driven redistribution)."
        ),
        comparison_years=[1980, 2000, 2014, 2023],
    ),
    DetectiveCase(
        id="land-ocean-contrast",
        title="Land Warms Faster: The Continental Amplification Effect",
        layer=DataLayer.TEMPERATURE,
        regions=["global_land", "global_ocean"],
        narrative=(
            "The global average temperature rise hides a stark divide: land "
            "surfaces warm roughly twice as fast as oceans, driving more extreme "
            "heat waves and permafrost thaw on land."
        ),
        explanation=(
            "Oceans have high heat capacity and mix warmth vertically, absorbing "
            "energy with less temperature change at the surface. Land has low heat "
            "capacity and no such mixing, so the same energy input raises its "
            "temperature much faster; polar land amplifies this further through "
            "ice-albedo feedback as snow cover shrinks."
        ),
        key_mechanism=(
            "Heat capacity contrast plus ice-albedo feedback drives differential warming."
        ),
        comparison_years=[1980, 2000, 2023],
    ),
]

QUESTIONS: List[DetectiveQuestion] = [
    DetectiveQuestion(
        id="q1",
        layer=DataLayer.SEA_ICE,
        region="arctic",
        question="How has Arctic sea ice extent changed since 1980?",
        options=[
            "Declined significantly (>10% per decade)",
            "Declined moderately (5-10% per decade)",
            "Remained roughly stable",
            "Increased slightly",
        ],
        correct_answer=0,
    ),
    DetectiveQuestion(
        id="q2",
        layer=DataLayer.SEA_ICE,
        region="antarctic",
        question="What was the Antarctic sea ice trend from 1980-2014?",
        options=[
            "Declined significantly",
            "Declined moderately",
            "Remained roughly stable",
            "Increased slightly",
        ],
        correct_answer=3,
    ),
    DetectiveQuestion(
        id="q3",
        layer=DataLayer.CO2,
        region="global",
        question="How has the atmospheric CO2 growth rate changed since 1980?",
        options=[
            "Slowed down",
            "Remained constant",
            "Accelerated",
            "Fluctuated with no clear pattern",
        ],
        correct_answer=2,
    ),
]


@router.get("/detective/cases", response_model=List[DetectiveCase])
def get_cases():
    return CASES


@router.get("/detective/mode/questions", response_model=List[DetectiveQuestion])
def get_questions():
    return QUESTIONS
