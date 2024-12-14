import time

from init import load_data

if __name__ == "__main__":
    shared_map, tester = load_data()

    ini_time = time.time()
    while time.time() - ini_time < 40:

        events = shared_map.copy()

        ids, values = map(list, zip(*[(k, 0 if v is None else v) for k, v in events.items()
                                                                 if isinstance(v, int) or v is None]))

        frame_data = [(k, v) for k, v in events.items() if not (isinstance(v, int) or v is None)]

        ids += [k for k, _ in frame_data]
        for id, event in zip(ids, values):
           tester.update_state_periferic(id, event)

        #xd = {periferico.idUniversal: periferic_to_inicialization(periferico) for periferico in tester.periferics}
