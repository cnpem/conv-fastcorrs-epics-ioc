#!/usr/bin/env python3

import epics
import time
import argparse


class SetpointLoadGenerator:
    def __init__(self, args):
        self.args = args
        self.pv_list = {}
        self.original_values = {}
        self.test_values = {}

    def generate_pv_list(self):
        pv_list = {}
        for sec in self.args.sector:
            for subsec in self.args.subsection:
                for pln in self.args.plane:
                    cell_str = f"{sec:02d}"
                    prefix = self.args.prefix
                    base = f"{prefix}SI-{cell_str}{subsec}:PS-{pln}:"
                    kick_sp = base + "Kick-SP"

                    # Create PV object
                    pv = epics.PV(kick_sp, auto_monitor=True)
                    pv_list[kick_sp] = pv

        return pv_list

    def wait_for_connection(self, timeout=10.0):
        start_time = time.time()
        disconnected_pvs = list(self.pv_list.keys())

        while disconnected_pvs and (time.time() - start_time < timeout):
            for pv_name in disconnected_pvs[:]:
                if self.pv_list[pv_name].connected:
                    disconnected_pvs.remove(pv_name)
            time.sleep(0.1)

        if disconnected_pvs:
            print(
                f"Warning: Timed out waiting for PVs to connect: {disconnected_pvs}")
            return False
        return True

    def prepare_test_values(self):
        for pv_name, pv in self.pv_list.items():
            if not pv.connected:
                print(f"Warning: PV {pv_name} is not connected")
                continue

            current_val = pv.get()

            drvl = pv.lower_ctrl_limit
            drvh = pv.upper_ctrl_limit

            self.original_values[pv_name] = current_val

            if current_val is not None and drvl is not None and drvh is not None:
                test_val1 = min(max(current_val + self.args.delta, drvl), drvh)
                test_val2 = min(max(current_val - self.args.delta, drvl), drvh)
                self.test_values[pv_name] = [test_val1, test_val2]
            else:
                print(f"Warning: Could not get valid values for {pv_name}")
                self.test_values[pv_name] = [current_val, current_val]

    def write_to_pv(self, pv_name, value):
        try:
            pv = self.pv_list[pv_name]
            if pv.connected:
                pv.put(value, wait=False)
                return True
            else:
                print(f"Warning: PV {pv_name} is not connected")
                return False
        except Exception as e:
            print(f"Error writing to {pv_name}: {e}")
            return False

    def mass_write(self, iteration):
        value_index = iteration % 2
        success_count = 0

        for pv_name in self.pv_list:
            if self.write_to_pv(pv_name, self.test_values[pv_name][value_index]):
                success_count += 1

        return success_count

    def restore_original_values(self):
        for pv_name, original_value in self.original_values.items():
            if original_value is not None and pv_name in self.pv_list:
                pv = self.pv_list[pv_name]
                if pv.connected:
                    pv.put(original_value, wait=True)

    def run_load_test(self):
        self.pv_list = self.generate_pv_list()

        if not self.wait_for_connection(timeout=10.0):
            print("Some PVs failed to connect. Continuing with available PVs.")

        self.prepare_test_values()

        print(f"Starting load test with {len(self.pv_list)} PVs")
        start_time = time.time()

        for i in range(self.args.iterations):
            start_writing = time.time()
            success_count = self.mass_write(i)
            if not self.args.quiet:
                print(f"Iteration {i+1}/{self.args.iterations}: "
                      f"Wrote to {success_count}/{len(self.pv_list)} PVs")

            end_writing = time.time() - start_writing
            if (self.args.interval > 0) and (end_writing < self.args.interval):
                time.sleep(self.args.interval - end_writing)

        elapsed_time = time.time() - start_time
        print(f"Load test completed in {elapsed_time:.2f} seconds")

        self.restore_original_values()


def main():
    parser = argparse.ArgumentParser(
        description="EPICS Setpoint Load Generator for CPU Load Testing")

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
    parser.add_argument("--iterations", type=int, default=100,
                        help="Number of mass write iterations")
    parser.add_argument("--interval", type=float, default=0.01,
                        help="Interval between iterations in seconds")

    parser.add_argument("--quiet", action="store_true",
                        help="Suppress progress output")

    args = parser.parse_args()

    generator = SetpointLoadGenerator(args)
    generator.run_load_test()


if __name__ == "__main__":
    main()
