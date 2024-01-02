import time
from skyfield.api import Topos, load

def find_visible_satellites(observer, tles, ts, time_utc):
    visible_satellites = []
    for name, line1, line2 in tles:
        satellite = load.tle(line1, line2, name=name)
        difference = satellite - observer
        topocentric = difference.at(time_utc)
        if topocentric.altaz()[0].degrees > 0:  # Altitude > 0 则视为可见
            visible_satellites.append(satellite.name)
    return visible_satellites

def main():
    # 加载 TLE 数据
    with open('guowang_tle.txt') as f:
        lines = f.readlines()
    tles = [lines[i:i+3] for i in range(0, len(lines), 3)]

    # 设置观察者位置（示例位置）
    observer = Topos('40.7128 N', '74.0060 W')

    # 创建时间对象
    ts = load.timescale()

    while True:
        time_utc = ts.now()  # 获取当前 UTC 时间
        visible_satellites = find_visible_satellites(observer, tles, ts, time_utc)
        print(f"Visible satellites at {time_utc.utc_datetime()} are: {visible_satellites}")

        time.sleep(60)  # 每分钟检查一次

if __name__ == '__main__':
    main()
