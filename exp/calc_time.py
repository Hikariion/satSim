# Given the downtime and recovery time for each experiment group, we need to calculate the recovery duration for each.
downtime_recovery_times = [
    (1710769406836, 1710769453141),
    (1710769591308, 1710769633902),
    (1710769707704, 1710769756953),
    (1710769915753, 1710769973113),
    (1710771364736, 1710771418903),
    (1710771525106, 1710771571680),
    (1710771650525, 1710771699172),
    (1710771714490, 1710771769542),
    (1710771785217, 1710771840650),
    (1710771886395, 1710771940070)
]

# Calculate recovery durations
recovery_durations = [(recovery - downtime) for downtime, recovery in downtime_recovery_times]

print(recovery_durations)
