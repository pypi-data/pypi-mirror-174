from datetime import timedelta
import numpy as np
import pandas as pd

from typing import Union, Dict, List, Optional, Literal, Annotated
from pydantic import validate_arguments, validator, BaseModel, conint, PositiveFloat, Field, validator, confloat 


# define the generic models
# - Numpy array
# - Numpy datetime
# - DS
# - DA
# - DAts

### Numpy array of a given type

class _TypedArray(np.ndarray):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        return np.array(val, dtype=cls.inner_type)

class _ArrayMeta(type):
    def __getitem__(self, t):
        if t in ['datetime', 'datetime64']:
            t = 'datetime64[ns]'
        return type('Array', (_TypedArray,), {'inner_type': t})

class NpArray(np.ndarray, metaclass=_ArrayMeta):
    pass
### Datetime and TimeDelta

class NpDatetime():
    """Model for datetime64
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update()

    @classmethod
    def validate(cls, v):
        v = np.datetime64(v, 'ns')
        if not isinstance(v, np.datetime64):
            raise TypeError('You must provide a valid datetime input (string, datetime, np.datetime)')
        return v
    def __repr__(self):
        return f'NpDatetime({super().__repr__()})'

class NpTimedelta():
    """Model for timedelta
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update()

    @classmethod
    def validate(cls, v):
        if isinstance(v, int):
            v = np.timedelta64(v, 'D')
        elif isinstance(v, timedelta):
            v = np.timedelta64(v, 'ns')
        if not isinstance(v, np.timedelta64):
            raise TypeError('You must provide a valid timedelta input (datetime.timedelta, np.datetime)')
        v = np.timedelta64(v, 'ns')
        return v
    def __repr__(self):
        return f'NpDatetime({super().__repr__()})'




class NpPeriod():
    """Model for Period
    Input must be a string, or a pd.Datetimeindex with correct frequency.
    If it is a string, it must be of the following formats
    - "date" -> provide a two dates pd.Datetimeindex date, date + 'D'
    - "date <f>" where <f> is one of 'D', 'W/W-FRI' (then week end friday) 'M/BM' (then Business month end), 'BQ/BQ-END/Q/Q-DEC' (then Business Quarter end) return a date, date +<f>
    - "date1 -> date1" provide a daterange from date1 to date2 with 'D' as frequency + one offset 'D' in the end.
    - "date1 -> date2 <f>" same as above for frequency (Note that it will only return the dates given frequency within this interval) + one with offset

    returns a pd.datetimeindex
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update()

    @classmethod
    def validate(cls, v):
        print(v)
        print(type(v))
        if isinstance(v, pd.DatetimeIndex) or isinstance(v, list):
            v = pd.DatetimeIndex(v, freq = 'infer')
            if v.freqstr not in {'B', 'W-FRI', 'BM', 'BQ-DEC'}:
                raise TypeError("If you provide a pd.Datetimeindex then the frequency must be one of 'B', 'W-FRI', 'BM', 'BQ-DEC', Q-DEC'")
            if len(v) <= 1:
                raise TypeError("If you provide a pd.Datetimeindex then at least two dates, it is an interval'")
        elif isinstance(v, str):
            # check first if we can split along ->
            parts = v.split('->')
            if len(parts) == 2:
                from_date = parts[0].strip()
                to_date = parts[1].split()
                periods = None
                if len(to_date) == 2:
                    frequency = to_date[1]
                    to_date = to_date[0]
                elif len(to_date) == 1:
                    frequency = 'B'
                    to_date = to_date[0]
                else:
                    raise TypeError("The string " + v + " does not satisfies the required format.")
            elif len(parts) == 1:
                from_date = parts[0].split()
                periods = 2
                to_date = None
                if len(from_date) == 2:
                    frequency = from_date[1]
                    from_date = from_date[0]
                elif len(from_date) == 1:
                    frequency = 'B'
                    from_date = from_date[0]
                else:
                    raise TypeError("The string " + v + " does not satisfies the required format.")
            else:
                raise TypeError("The string " + v + " does not satisfies the required format.")

            # Now we check for the validity of the frequency
            if 'D' in frequency or frequency == 'B':
                frequency = 'B'
            elif 'W' in frequency:
                frequency = 'W-FRI'
            elif 'M' in frequency:
                frequency = 'BM'
            elif 'Q' in frequency:
                frequency = 'BQ-DEC'
            else:
                raise TypeError("The string " + v + " does not satisfies the required format.")

            if frequency == 'B':
                from_date = pd.to_datetime(from_date) + pd.offsets.Day(1) - pd.offsets.BDay(1) #get the closest previous business day
                if to_date is not None:
                    to_date = pd.to_datetime(to_date) + pd.offsets.BDay(1)
            elif frequency == 'W-FRI':
                from_date = (pd.to_datetime(from_date) - pd.offsets.Week(1)) + pd.offsets.Week(0, weekday = 4) #get the closest first business day of the previous week
                if to_date is not None:
                    to_date = pd.to_datetime(to_date) + pd.offsets.Week(1, weekday = 5)
            elif frequency == 'BM':
                from_date = pd.to_datetime(from_date) + pd.offsets.BMonthEnd(1) - pd.offsets.BMonthEnd(1) #get the closest last business day of the previous month
                if to_date is not None:
                    to_date = pd.to_datetime(to_date) + pd.offsets.BMonthEnd(1)
            elif frequency == 'BQ-DEC':
                from_date = pd.to_datetime(from_date) + pd.offsets.BQuarterEnd(1) - pd.offsets.BQuarterEnd(1) #get the closest previous business day
                if to_date is not None:
                    to_date = pd.to_datetime(to_date) + pd.offsets.BQuarterEnd(1)
            # Now we are in place to construct out datetime index
            try:
                v = pd.date_range(start = from_date, end = to_date, periods = periods, freq = frequency)
            except:
                raise TypeError("The string " + v + " does not satisfies the required format.")
        else:
            raise TypeError("The string " + v + " does not satisfies the required format.")
        if len(v) <=1:
            raise TypeError("The period should contain at least tow dates.")
        return v
    def __repr__(self):
        return f'NpDateRange({super().__repr__()})'

class NpPeriodModel(BaseModel):
    v: NpPeriod





## Model for strategy functions

class StrategyModel(BaseModel):
    input_var: Optional[Union[str, List[str],  Dict]] = None
    window: Optional[conint(ge=0, le=7)] = None
    selfw: Optional[bool] = False
    vectorize: Optional[bool] = False
    from_date: Optional[NpDatetime]
    to_date: Optional[NpDatetime]
    freq: Optional[Literal['W', 'M', 'Q', 'Y']] = None

    @validator('input_var')
    def input_vars_validate(cls, v):
        if isinstance(v, str):
            result = {v : ['value']}
        elif isinstance(v, list):
            tmp = {}
            for k in v:
                tmp[k] = ['value']
            v = tmp
        return v


class TCostModel(BaseModel):
    fees: PositiveFloat = 0.0002
    tax: PositiveFloat = 0.001




### Distributions
# Using Annotated we nest the different distributions with default Normal distribution.
# Define the class models for each distribution

class DistNModel(BaseModel):
    name: Literal['N', 'n', 'norm', 'Norm', 'gaussian', 'Gaussian', 'standart', 'Standart'] = 'N'
    loc: float = 0.0
    scale: confloat(gt = 0) = 1.0

    @validator('name')
    def instrumentid_valid(cls, v):
        # Normalize name to N
        v = 'N'
        return v

class DistTModel(BaseModel):
    name: Literal['T', 't', 'Student', 'student', 'Studentt', 'studentt'] = 'T'
    loc: float = 0.0
    scale: confloat(gt = 0) = 1.0
    df: confloat(ge = 2.0) = 2.0

    @validator('name')
    def instrumentid_valid(cls, v):
        # Normalize name to N
        v = 'T'
        return v

Dist = Annotated[Union[DistNModel, DistTModel], Field(discriminator = 'name')]

class DistModel(BaseModel):
    dist: Optional[Dist] = DistNModel()


