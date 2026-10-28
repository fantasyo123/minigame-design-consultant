#!/usr/bin/env python3
"""Validate the configuration and run one deterministic reference route per level.
No third-party dependencies. This is a model, not an engine/device test.
"""
import json, math, pathlib, sys
p=pathlib.Path(__file__).with_name('levels.json')
d=json.loads(p.read_text(encoding='utf-8'))
levels=d['levels']; errors=[]
def check(ok,msg):
    if not ok: errors.append(msg)
check(d['schemaVersion']=='1.0.0','schemaVersion')
check([l['id'] for l in levels]==list(range(1,21)),'IDs must be 1..20 in order')
allowed={'jump','static_obstacle','consecutive_jump','coins','moving_obstacle','speed_zone'}
for l in levels:
    tag='level '+str(l['id']); ms=set(l['mechanics']); obs=l['obstacles']; coins=l['coins']; zones=l['speedZones']; jump=l['jump']; length=l['length']; v=l['baseSpeed']
    check(ms<=allowed and len(ms)==len(l['mechanics']),tag+' unknown/duplicate mechanism')
    check({'jump','static_obstacle'}<=ms,tag+' base mechanisms')
    check(20<=length<=65 and 2.5<=v<=3.5,tag+' length/speed range')
    check(4.5<=jump['initialVelocity']<=6 and 12<=jump['gravity']<=16,tag+' jump range')
    check(0<=jump['coyoteSeconds']<=.15 and 0<=jump['bufferSeconds']<=.15,tag+' jump assistance')
    check(0<=l['maxMistakes']<=2 and 0<=l['coinsRequired']<=len(coins),tag+' objectives')
    check(10<=l['timeLimitSeconds']<=45 and 0<=l['targetFailureRatePercent']<=100,tag+' time/target')
    check(l['reward']['completionCoins']>0,tag+' reward')
    check(l['obstacleDensityPer10']==round(len(obs)/length*10,2),tag+' density')
    check(('moving_obstacle' in ms)==any(o['type']=='moving' for o in obs),tag+' moving dependency')
    check(('speed_zone' in ms)==bool(zones),tag+' speed dependency')
    check(('coins' in ms)==bool(coins),tag+' coins mechanic dependency')
    check('consecutive_jump' not in ms or len(obs)>=2,tag+' consecutive dependency')
    check(all(o['type'] in ('static','moving') and 0<o['x']<length and .2<=o['width']<=.6 and .2<=o['height']<=.5 for o in obs),tag+' obstacle range')
    check([o['x'] for o in obs]==sorted(o['x'] for o in obs) and len({o['x'] for o in obs})==len(obs),tag+' obstacle order')
    check(all(0<c['x']<length and 0<c['y']<=1.5 and 0<c['radius']<=.3 for c in coins),tag+' coin range')
    check(len({x['id'] for x in obs+coins+zones})==len(obs+coins+zones),tag+' duplicate object ID')
    for o in obs:
        if o['type']=='moving': check(0<o['liftAmplitude']<=.2 and 1<=o['periodSeconds']<=4 and 0<=o['phaseRadians']<=2*math.pi,tag+' moving params')
    for z in zones: check(0<=z['startX']<z['endX']<=length and 1<=z['speedMultiplier']<=1.1,tag+' zone params')
    check(all(a['endX']<=b['startX'] for a,b in zip(zones,zones[1:])),tag+' zone overlap')
    # Model one tap before each hazard; physics continuous within fixed steps.
    dt=1/120; t=0.; x=0.; y=0.; vy=0.; collected=set(); hit=set(); tapped=set()
    while t<=l['timeLimitSeconds'] and x<length:
        multiplier=next((z['speedMultiplier'] for z in zones if z['startX']<=x<z['endX']),1)
        speed=v*multiplier
        for o in obs:
            if o['id'] not in tapped and x>=o['x']-speed*(jump['initialVelocity']/jump['gravity']):
                if y<=1e-8: vy=jump['initialVelocity']; tapped.add(o['id'])
        x+=speed*dt
        y+=vy*dt-.5*jump['gravity']*dt*dt; vy-=jump['gravity']*dt
        if y<0: y=0.; vy=0.
        t+=dt
        for o in obs:
            lift=o.get('liftAmplitude',0)*(1-math.cos(2*math.pi*t/o.get('periodSeconds',1)+o.get('phaseRadians',0)))/2
            if abs(x-o['x'])<(d['global']['playerWidth']+o['width'])/2 and y<lift+o['height'] and y+d['global']['playerHeight']>lift: hit.add(o['id'])
        for c in coins:
            dx=max(abs(c['x']-x)-d['global']['playerWidth']/2,0); dy=max(abs(c['y']-(y+d['global']['playerHeight']/2))-d['global']['playerHeight']/2,0)
            if dx*dx+dy*dy<=c['radius']**2: collected.add(c['id'])
    check(x>=length and t<=l['timeLimitSeconds'] and len(hit)<=l['maxMistakes'] and len(collected)>=l['coinsRequired'],tag+f' reference route fails (x={x:.2f}, t={t:.2f}, hits={len(hit)}, coins={len(collected)})')
if errors:
    print('\n'.join('ERROR '+x for x in errors)); sys.exit(1)
print(f'PASS: {len(levels)} levels; IDs, ranges, object IDs, mechanism dependencies, density, targets and 20 modeled reference routes')
