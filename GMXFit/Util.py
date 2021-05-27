
def fixAngleRange(angle):
    # wrap periodic angle from -180 to 180 
    while angle > 180 or angle < -180:
        if angle > 180:
            angle -= 360
        elif angle < -180:
            angle += 360
    return angle
