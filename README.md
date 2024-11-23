# Race Predictor
A machine learning project that analyses trends in similar tracks to predict the winner of a certain Grand Prix.

## How it works
The aim is to predict the winner of a certain Grand Prix. This predictor will determine this using the following:
- Detect trends in performance at certain tracks to determine which constructors perform well at certain types of tracks
- Previous performance at each track
- Current form of constructors and drivers
- Reliability of constructors
- Driver's crash rate
- Likelihood of jeopardy
  - Are there many DNFs here previously?
  - Is rain likely to make an appearance?

## Constructor Reliability
Reliability is calculated using the following:  
```python
reliability = (total_entries - total_mechanical_dnfs) / total_entries
```

It is important to decipher whether a car DNF was due to a mechanical failure or by a driver's fault.
I excluded any DNF reasons that where not mechanical related. Reliability as a whole may not be a reliable factor for this project.
For example, it is unfair to use reliability statistics from 2014 to predict races in 2024.
Therefore, I calculated the reliability for the year for each constructor, calculating a more recent and relevant variable.

## Driver Crash Rate
Driver crash rate is calculated similarly to Constructor Reliability:
```python
crash_rate = 1 - ((total_entries - total_driver_fault_dnfs) / total_entries)
```

Again, it is important to decipher whether the DNF was a driver's fault.
I did the opposite of calculating the reliability and only included DNFs that were reported as a driver's fault.
This only includes crashes and damage related DNFs.
As with reliability, I also calculated each driver's crash rate by season for better accuracy and relevancy.

## Constructor & Drivers Current Form
It is important to know the current form for a constructor when attempting to how they will do in the next race.
To calculate the current form, the positions from the previous 6 races are taken and applied to the following points system:
- DNF = 0 points
- P20 = 1 point
- P19 = 2 points
- P18 = 3 points
- P17 = 4 points
- P16 = 5 points
- P15 = 6 points
- P14 = 7 points
- P13 = 8 points
- P12 = 9 points
- P11 = 10 points
- P10 = 11 points
- P9  = 12 points
- P8  = 13 points
- P7  = 14 points
- P6  = 15 points
- P5  = 16 points
- P4  = 17 points
- P3  = 18 points
- P2  = 19 points
- P1  = 20 points

Current form is calculated using the points system above and taken the average over the past 6 races.
This provides an accurate representation of how a driver or constructor is performing coming into the next race.

## Track similarities
Finding trends in performances between constructors and tracks will be beneficial in predicting more accurate results.
For each race at each track, the constructors are scored using the points system above.
They are then scored on how many positions higher or lower they finished compared to their position in the standings.

Trends can then be identified between the tracks based on these performances.
For example, if the same constructors that scored a high result in Monaco also scored a high result in Hungary,
we could assume that the winners of Monaco next season would have a high chance of winning Hungary too.
