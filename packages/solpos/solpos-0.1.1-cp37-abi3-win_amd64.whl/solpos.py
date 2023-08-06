from typing import NamedTuple

from _solpos import _solpos


class SolposResult(NamedTuple):
    """Container for the results returned by :func:`solpos.solpos`.

    :param year: 4-digit year
    :param month: Month number (Jan = 1, Feb = 2, etc.)
    :param day: Day of month (May 27 = 27, etc.)
    :param hour: Hour of day, 0 - 24. (Time 24:00:00 is treated internally as
        time 00:00:00 of the following day.)
    :param minute: Minute of hour, 0 - 59
    :param second: Second of minute, 0 - 59
    :param timezone: Time zone, east (west negative). USA: Mountain = -7, Central = -6, etc.
    :param latitude: Latitude, *degrees* north (south negative)
    :param longitude: Longitude, *degrees* east (west negative)
    :param interval: Interval of a measurement period in *seconds*
    :param aspect: Azimuth of panel surface in *degrees* (direction it faces)
        N=0, E=90, S=180, W=270.
    :param press: Surface pressure, *millibars*
    :param sbwid: Shadow-band width (*cm*)
    :param sbrad: Shadow-band radius (*cm*)
    :param sbsky: Shadow-band sky factor (-1 - 1)
    :param solcon: Solar constant (*W/m²*)
    :param temp: Ambient dry-bulb temperature, *degrees C*
    :param tilt: *Degrees* tilt from horizontal of panel (-180 - 180)
    :param amass: Relative optical airmass
    :param ampress: Pressure-corrected airmass
    :param azim: Solar azimuth angle (*degrees*): N=0, E=90, S=180,W=270
    :param cosinc: Cosine of solar incidence angle on panel
    :param coszen: Cosine of refraction corrected solar zenith angle
    :param dayang: Day angle :math:`\\frac{daynum * 360}{year\\_length}`, *degrees*
    :param declin: Declination-zenith angle of solar noon at equator *degrees NORTH*
    :param eclong: Ecliptic longitude, *degrees*
    :param ecobli: Obliquity of ecliptic
    :param ectime: Time of ecliptic calculations
    :param elevetr: Solar elevation, no atmospheric correction (= ETR)
    :param elevref: Solar elevation angle, *degrees* from horizon, refracted
    :param eqntim: Equation of time (TST - LMT), *minutes*
    :param erv: Earth radius vector(multiplied to solar constant)
    :param etr: Extraterrestrial (top-of-atmosphere) *W/m²* global horizontal solar irradiance
    :param etrn: Extraterrestrial (top-of-atmosphere) *W/m²* direct normal solar irradiance
    :param etrtilt: Extraterrestrial (top-of-atmosphere) *W/m²* global irradiance on a tilted surface
    :param gmst: Greenwich mean sidereal time, *hours*
    :param hrang: Hour angle--hour of sun from solar noon *degrees WEST*
    :param julday: Julian Day of 1 JAN 2000 minus 2,400,000 days (in order to regain single precision)
    :param lmst: Local mean sidereal time, *degrees*
    :param mnanom: Mean anomaly, *degrees*
    :param mnlong: Mean longitude, *degrees*
    :param rascen: Right ascension, *degrees*
    :param press: Surface pressure, *millibars*, used for refraction correction and ``ampress``
    :param prime: Factor that normalizes :math:`K_t`, :math:`K_n`, etc.
    :param sbcf: Shadow-band correction factor
    :param sbwid: Shadow-band width (*cm*)
    :param sbrad: Shadow-band radius (*cm*)
    :param sbsky: Shadow-band sky factor
    :param solcon: Solar constant, *W/m²*
    :param ssha: Sunset(/rise) hour angle, *degrees*
    :param sretr: Sunrise time, minutes from midnight, local, **without** refraction
    :param ssetr: Sunset time, minutes from midnight, local, **without** refraction
    :param temp: Ambient dry-bulb temperature, *degrees C*, used for refraction correction
    :param tilt: *Degrees* tilt from horizontal of panel
    :param tst: True solar time, *minutes* from midnight
    :param tstfix: True solar time - local standard time
    :param unprime: Factor that denormalizes :math:`K_t'`, :math:`K_n'`, etc.
    :param utime: Universal (Greenwich) standard time
    :param zenetr: Solar zenith angle, no atmospheric correction (= ETR)
    :param zenref: Solar zenith angle, *degrees* from zenith, refracted.
    """  # noqa: E501
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: float
    timezone: float
    interval: int
    latitude: float
    longitude: float
    amass: float
    ampress: float
    aspect: float
    azim: float
    cosinc: float
    coszen: float
    dayang: float
    declin: float
    eclong: float
    ecobli: float
    ectime: float
    elevetr: float
    elevref: float
    eqntim: float
    erv: float
    etr: float
    etrn: float
    etrtilt: float
    gmst: float
    hrang: float
    julday: float
    lmst: float
    mnanom: float
    mnlong: float
    rascen: float
    press: float
    prime: float
    sbcf: float
    sbwid: float
    sbrad: float
    sbsky: float
    solcon: float
    ssha: float
    sretr: float
    ssetr: float
    temp: float
    tilt: float
    tst: float
    tstfix: float
    unprime: float
    utime: float
    zenetr: float
    zenref: float


def solpos(
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        timezone: float,
        *,
        latitude: float,
        longitude: float,
        interval: int = 0,
        aspect: float = 180.0,
        press: float = 1013.0,
        sbwid: float = 7.6,
        sbrad: float = 31.7,
        sbsky: float = 0.04,
        solcon: float = 1367.0,
        temp: float = 15.0,
        tilt: float = 0.0,
) -> SolposResult:
    """Computes the solar position and intensity from time and place.

    The underlying ``posdata pdat->function`` struct is set to ``S_ALL``
    meaning all possible parameters are calculated using the defaults or the
    user defined values.

    :param year: 4-digit year (2-digit years are **NOT** allowed)
    :param month: Month number (Jan = 1, Feb = 2, etc.)
    :param day: Day of month (May 27 = 27, etc.)
    :param hour: Hour of day, 0 - 24. (Time 24:00:00 is treated internally as
        time 00:00:00 of the following day.)
    :param minute: Minute of hour, 0 - 59
    :param second: Second of minute, 0 - 59
    :param timezone: Time zone, east (west negative). USA: Mountain = -7,
        Central = -6, etc.
    :param latitude: Latitude, *degrees* north (south negative)
    :param longitude: Longitude, *degrees* east (west negative)
    :param interval: Interval of a measurement period in *seconds*. Forces
        solpos to use the time and date from the interval midpoint. The input
        time (``hour``, ``minute``, and ``second``) is assumed to be the
        **END** of the measurement interval (right labelled) (default: ``0.0``)
    :param aspect: Azimuth of panel surface in *degrees* (direction it faces)
        N=0, E=90, S=180, W=270. (default: ``180.0``)
    :param press: Surface pressure, *millibars*, used for refraction correction
        and ampress (default: ``1013.0``)
    :param sbwid: Shadow-band width (*cm*) (default: ``7.6``)
    :param sbrad: Shadow-band radius (*cm*) (default: ``31.7``)
    :param sbsky: Shadow-band sky factor (-1 - 1) (default: ``0.04``)
    :param solcon: Solar constant (NREL uses 1367 *W/m²*) (default: ``1367.0``)
    :param temp: Ambient dry-bulb temperature, *degrees C*, used for refraction
        correction (default: ``15.0``)
    :param tilt: *Degrees* tilt from horizontal of panel (-180 - 180)
        (default: ``0.0``)

    :return: A :func:`solpos.SolposResult` object with all parameters that
        SOLPOS is able to calculate (including all input parameters)
    """
    result = _solpos(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        timezone=timezone,
        latitude=latitude,
        longitude=longitude,
        interval=interval,
        aspect=aspect,
        press=press,
        sbwid=sbwid,
        sbrad=sbrad,
        sbsky=sbsky,
        solcon=solcon,
        temp=temp,
        tilt=tilt,
    )
    return SolposResult(**result)
