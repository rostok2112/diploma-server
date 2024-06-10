import json
import numpy as np
from environment import settings
from worker.utils import compute_euler_angles


async def process_complementary_filter(data, redis_conn):
    X, Y, Z = list(range(3))
    
    TAU = settings.TAU
    DT  = settings.DT
    
    euler_degs = await redis_conn.get('euler_degs') or '{}'
    euler_degs = json.loads(euler_degs)
    
    euler_degs_r = euler_degs.get('r', 0.0)
    euler_degs_p = euler_degs.get('p', 0.0)
    euler_degs_y = euler_degs.get('y', 0.0)
    
    # Преобразование списков в массивы NumPy
    data_A = np.array(data['A'])
    data_G = np.array(data['G'])
    
    degs_r, degs_p, degs_y = compute_euler_angles(
        data_A, data_G, euler_degs_r, euler_degs_p, euler_degs_y, TAU, DT
    )
    
    degs = {
        'r': degs_r, 
        'p': degs_p, 
        'y': degs_y,
    }
    
    await redis_conn.set('euler_degs', json.dumps(degs))
    