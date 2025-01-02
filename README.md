# Race Predictor
A machine learning project that analyses trends in similar tracks to predict the winner of a certain Grand Prix.

## How it works
The aim is to predict the winner of a certain Grand Prix. This predictor will determine this using the following:
- Detect trends in performance at certain tracks to determine which constructors perform well at certain tracks
- Previous performance at each track
- Current form of constructors and drivers
- Reliability of constructors
- Driver's crash rate

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
crash_rate = ((total_entries - total_driver_fault_dnfs) / total_entries) / 100
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

## Track specific performances
Finding trends in performances between constructors and tracks will be beneficial in predicting more accurate results.
For each race at each track, the constructors are scored using the points system above.
They are then scored on how many positions higher or lower they finished compared to their position in the standings.

Therefore, when predicting at certain tracks, we can use this historical data to determine whether a constructor's car suits this track.
The same method was also applied to the drivers to determine how suited a driver is to specific tracks.

## Training model
First, I tried using a Linear Regression model. This was highly unreliable and provided very inaccurate results.
Next, I implemented a Logistic Regression model. This should have been more suited to the prediction style of the project but its accuracy was as low as 30%.  

It was then suggested to try a Random Forest Classifier model. This was easily integrated into the project and provided a much higher accuracy.
The current accuracy is around 87-89%.

## Weightings
At first, I was using a Min Max Scaler to scale the data to stop one column from overpowering the others. This resulted in strange anomalies.
I believe this was due to certain backmarker drivers and constructors regularly having a high track performance which made them appear stronger than they actually were.
For example, RB was regularly appearing in the top 3 teams in the predictions, yet they were not a podium contending constructor.  

As a result, I removed the Min Max Scaler and applied my own weightings.
I found that applying a higher weighting to constructor form provided the best results.

## Conclusion
Formula One can usually be predicted. There is usually one team that dominates and the rest of the order can sometimes be just as easily predicted.
However, I have created this project at the end of 2024 season which has not been an easily predictable season.
It has been rather difficult to predict which team will be fastest for each race.  

Constructor form plays a large role in these predictions. Crashes and mechanical DNFs do not occur very often as of recently.
Therefore, higher weightings have been applied to constructor forms and track performances based on historical data to provide the most accurate results.  

I am looking forward to applying this predictive model for 2025 season. I will record real world accuracies here.