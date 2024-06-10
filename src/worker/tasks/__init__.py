import json
from math import atan2, degrees
from environment import settings


async def process_complementary_filter(data, redis_conn):
    X, Y, Z = list(range(3))
    
    TAU = settings.TAU
    DT  = settings.DT
    
    euler_degs = await redis_conn.get('euler_degs') or '{}'
    euler_degs = json.loads(euler_degs)
    
    accel_pitch = degrees(atan2(data['A'][Y], data['A'][Z]));
    accel_roll  = degrees(atan2(data['A'][X], data['A'][Z]));

    
    degs = {
        'r': TAU * (euler_degs.get('r', 0.0) - data['G'][Y] * DT) + (1 - TAU) * accel_roll, 
        'p': TAU * (euler_degs.get('p', 0.0)  + data['G'][X] * DT) + (1 - TAU) * accel_pitch, 
        'y': euler_degs.get('y', 0.0) + data['G'][Z] * DT,
    }
    
    await redis_conn.set('euler_degs', json.dumps(degs))
    