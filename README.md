# Race Predictor
**A machine learning project that analyses trends in similar tracks to predict the winner of a certain Grand Prix.**  

## How it works
The aim is to predict the winner of a certain Grand Prix. This predictor will determine this using the following:
- Detect trends in performance at certain tracks to determine which constructors perform well at certain types of tracks
- Previous performance at each track
- Current form of constructors and drivers
- Reliability of constructors
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