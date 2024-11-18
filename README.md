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