#!/usr/bin/env python3

import epics
import time
import argparse
import csv
import threading
from collections import defaultdict


class PropagationDelayMeasurer:
    def __init__(self, args):
        self.args = args
        self.measurement_lock = threading.Lock()
        self.active_measurements = {}
        self.completion_events = {}
        self.pv_callbacks = {}

    def generate_pv_names(self):
        pv_sets = []
        for sec in self.args.sector:
            for subsec in self.args.subsection:
                for pln in self.args.plane:
                    cell_str = f"{sec:02d}"
                    prefix = self.args.prefix
                    base = f"SI-{cell_str}{subsec}:PS-{pln}:"

                    kick_sp = prefix + base + "Kick-SP"
                    current_sp = base + "Current-SP"
                    current_rb = base + "Current-RB"
                    kick_rb = prefix + base + "Kick-RB"
                    current_mon = base + "Current-Mon"
                    kick_mon = prefix + base + "Kick-Mon"

                    pv_sets.append((
                        kick_sp, current_sp,
                        current_rb, kick_rb,
                        current_mon, kick_mon,
                        sec, subsec, pln
                    ))
        return pv_sets

    def wait_for_connection(self, pv_list, timeout=10.0):
        start_time = time.time()
        disconnected_pvs = list(pv_list)

        while disconnected_pvs and (time.time() - start_time < timeout):
            for pv_name in disconnected_pvs[:]:
                if pv_name in self.pv_objects and self.pv_objects[pv_name].connected:
                    disconnected_pvs.remove(pv_name)
            time.sleep(0.1)

        if disconnected_pvs:
            print(
                f"Warning: Timed out waiting for PVs to connect: {disconnected_pvs}")
            return False
        return True

    def create_pv_callback(self, pair_type):
        def callback(pvname, value, timestamp, **kwargs):
            with self.measurement_lock:
                if pvname not in self.active_measurements:
                    return

                meas = self.active_measurements[pvname]

                # Record the timestamp for this pair type
                meas['timestamps'][pair_type] = timestamp

                if (meas['timestamps']['kick_sp'] is not None and
                        meas['timestamps']['kick_mon'] is not None):
                    event = self.completion_events.get(meas['id'])
                    if event:
                        event.set()
        return callback

    def measure_for_pv(self, kick_sp, current_sp, current_rb,
                       kick_rb, current_mon, kick_mon,
                       sec, subsec, pln):
        pv_names = [
            kick_sp, current_sp, current_rb, kick_rb, current_mon, kick_mon
        ]

        self.pv_objects = {}
        for pv in pv_names:
            self.pv_objects[pv] = epics.PV(pv, auto_monitor=True)
            if pv == kick_sp:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("kick_sp"))
            elif pv == current_sp:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("current_sp"))
            elif pv == current_rb:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("current_rb"))
            elif pv == kick_rb:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("kick_rb"))
            elif pv == current_mon:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("current_mon"))
            elif pv == kick_mon:
                self.pv_objects[pv].add_callback(
                    self.create_pv_callback("kick_mon"))

        # Wait for connection
        if not self.wait_for_connection(pv_names):
            return [(None, None, None)] * self.args.iterations

        # Get limit values using PV objects
        drvl = self.pv_objects[kick_sp].lower_ctrl_limit
        drvh = self.pv_objects[kick_sp].upper_ctrl_limit
        orig_sp = self.pv_objects[kick_sp].get()

        # Determine test value
        test_vals = [orig_sp + self.args.delta, orig_sp - self.args.delta]
        test_value = next((v for v in test_vals if drvl <= v <= drvh), None)
        if test_value is None:
            return [(None, None, None)] * self.args.iterations

        delays = []
        for iter_num in range(self.args.iterations):
            measurement_id = f"{sec}-{subsec}-{pln}-{iter_num}"
            event = threading.Event()
            self.completion_events[measurement_id] = event

            meas = {
                'id': measurement_id,
                'timestamps': defaultdict(lambda: None)
            }

            with self.measurement_lock:
                for pv in pv_names:
                    self.active_measurements[pv] = meas

            # Apply test value using PV object
            self.pv_objects[kick_sp].put(test_value, wait=False)

            # Wait for completion
            event.wait(self.args.timeout)

            # Calculate delays
            ts = meas['timestamps']
            cmd_prop_delay = ts['current_sp'] - \
                ts['kick_sp'] if ts['current_sp'] else None
            fbk_processing_delay = ts['kick_rb'] - \
                ts['current_rb'] if ts['kick_rb'] and ts['current_rb'] else None
            mon_refresh_delay = ts['kick_mon'] - \
                ts['current_mon'] if ts['kick_mon'] and ts['current_mon'] else None

            delays.append(
                (cmd_prop_delay, fbk_processing_delay, mon_refresh_delay))

            # Reset to original value
            self.pv_objects[kick_sp].put(orig_sp, wait=True)

            # Cleanup
            with self.measurement_lock:
                for pv in pv_names:
                    if pv in self.active_measurements:
                        del self.active_measurements[pv]
                if measurement_id in self.completion_events:
                    del self.completion_events[measurement_id]

        # Disconnect PVs
        for pv in self.pv_objects.values():
            pv.disconnect()
        del self.pv_objects

        return delays

    def run_measurements_sequential(self, pv_sets):
        with open(self.args.output, "w", newline="") as csvfile:
            fieldnames = [
                "sec", "subsec", "plane", "iteration",
                "cmd_prop_delay", "fbk_processing_delay", "mon_refresh_delay"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for idx, pv_set in enumerate(pv_sets):
                sec, subsec, pln = pv_set[6:]
                if not self.args.quiet:
                    print(
                        f"[{idx+1}/{len(pv_sets)}] Sector {sec} {subsec} {pln}...")

                delays = self.measure_for_pv(*pv_set)

                for iter_num, delays_tuple in enumerate(delays):
                    writer.writerow({
                        "sec": sec,
                        "subsec": subsec,
                        "plane": pln,
                        "iteration": iter_num,
                        "cmd_prop_delay": delays_tuple[0],
                        "fbk_processing_delay": delays_tuple[1],
                        "mon_refresh_delay": delays_tuple[2]
                    })

    def run_measurements(self):
        pv_sets = self.generate_pv_names()
        self.run_measurements_sequential(pv_sets)

        if not self.args.quiet:
            print(f"Data saved to {self.args.output}")


def main():
    parser = argparse.ArgumentParser(
        description="EPICS Control System Propagation Delay Measurement")

    parser.add_argument("--sector", type=int, nargs="+", default=list(range(1, 21)),
                        help="Sector numbers (e.g., '1 2 3' or '1..20')")
    parser.add_argument("--subsection", nargs="+", default=["M1", "M2", "C2", "C3"],
                        help="Subsection types (e.g., 'M1 M2')")
    parser.add_argument("--plane", nargs="+", default=["FCV", "FCH"],
                        help="Plane types (e.g., 'FCV FCH')")
    parser.add_argument("--prefix", default="",
                        help="Test prefix for PVs")

    parser.add_argument("--delta", type=float, default=0.01,
                        help="Setpoint change delta")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="Measurement timeout (s)")
    parser.add_argument("--iterations", type=int, default=10,
                        help="Iterations per PV")

    parser.add_argument("--output", default="propagation_delays.csv",
                        help="Output CSV filename")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress output")

    args = parser.parse_args()

    if not args.quiet:
        print(f"Starting propagation delay measurements for {len(args.sector)} sectors, "
              f"{len(args.subsection)} subsections, {len(args.plane)} planes")
        print(f"Configuration: delta={args.delta} "
              f"timeout={args.timeout} iterations={args.iterations}")

    measurer = PropagationDelayMeasurer(args)
    measurer.run_measurements()


if __name__ == "__main__":
    main()
